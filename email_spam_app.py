import streamlit as st
import sqlite3
import bcrypt
import pickle

# Load your ML model and vectorizer
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Load CSS from file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (email TEXT PRIMARY KEY, username TEXT, password BLOB)''')
conn.commit()

# Add user to DB with hashed password
def add_user(email, username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
                  (email, username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Verify user password and get username
def verify_user(email, password):
    c.execute('SELECT username, password FROM users WHERE email = ?', (email,))
    record = c.fetchone()
    if record:
        username, stored_password = record
        if bcrypt.checkpw(password.encode(), stored_password):
            return True, username
    return False, None

# Check if user exists
def user_exists(email):
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    return c.fetchone() is not None

# Background for main app page ONLY
def set_background():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: url("https://static.vecteezy.com/system/resources/thumbnails/008/962/769/small/abstract-red-silver-cyber-grey-metallic-geometric-gold-light-on-black-hexagon-mesh-design-modern-technology-futuristic-background-vector.jpg") no-repeat center center fixed;
            background-size: cover;
        }
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Reset background for login/signup pages
def reset_background():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: none !important;
        }
        [data-testid="stAppViewContainer"]::before {
            background: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Login form
def login():
    reset_background()  # Remove main app background for login page

    with st.form("login_form"):
        st.markdown('<h2>Login</h2>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Email", key="login_email")
        password = st.text_input("", placeholder="Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

    if submit:
        if not email or not password:
            st.warning("Please fill in all fields.")
        else:
            success, username = verify_user(email, password)
            if success:
                st.success(f"Welcome back, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['user_email'] = email
                st.session_state['username'] = username
            else:
                st.error("Invalid credentials.")

# Signup form
def signup():
    reset_background()

    st.subheader("Create a New Account")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if not email or not username or not password or not password2:
            st.warning("Please fill in all fields.")
        elif password != password2:
            st.warning("Passwords do not match.")
        elif user_exists(email):
            st.warning("Email already registered.")
        else:
            success = add_user(email, username, password)
            if success:
                st.success("Account created successfully! Please log in.")
                st.session_state['page'] = 'login'
            else:
                st.error("Failed to create account. Try again.")

# Logout function
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.info("You have been logged out. Please refresh the page if necessary.")

# Main app after login
def main_app():
    set_background()

    st.markdown('<div id="main-app-container">', unsafe_allow_html=True)

    # Personalized welcome
    st.markdown(
    f"""
    <div class="fade-message">
        Welcome, <span style='color: #00ffcc;'>{st.session_state['username']}</span>!
    </div>
    """,
    unsafe_allow_html=True
)


    st.markdown('<h1 class="vintage-title" data-text="Email Spam Detector">Email Spam Detector</h1>', unsafe_allow_html=True)

    email_text = st.text_area("", height=200, placeholder="Paste your email content here...")

    if st.button("Predict"):
        if email_text.strip() == "":
            st.warning("⚠️ Please enter some text to analyze!")
        else:
            transformed_text = vectorizer.transform([email_text])
            prediction = model.predict(transformed_text)[0]
            if prediction == 1:
                st.success("✅ This email is classified as **NOT SPAM**!", icon="✅")
            else:
                st.error("🚨 This email is classified as **SPAM**!", icon="🚨")

    if st.button("Logout"):
        logout()

    st.markdown('</div>', unsafe_allow_html=True)

# Main entry point
def main():
    # Inject Google Fonts
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Load your custom CSS
    local_css("style.css")

    # Session state init
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['logged_in']:
        main_app()
    else:
        st.sidebar.title("Navigation")
        option = st.sidebar.radio("Go to", ["Login", "Sign Up"])
        st.session_state['page'] = option.lower()

        if st.session_state['page'] == 'login':
            login()
        elif st.session_state['page'] == 'sign up':
            signup()

if __name__ == "__main__":
    main()
