# email_spam_app.py

import streamlit as st
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load your trained model and vectorizer
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Page config+
st.set_page_config(page_title="Email Spam Detector", page_icon="📧", layout="wide")

# Stylish Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>📧 Email Spam Detection</h1>", 
    unsafe_allow_html=True
)

st.write("### Enter the email text below:")

# Email input
email_text = st.text_area("", height=200, placeholder="Paste your email content here...")

# Predict Button
if st.button('Predict', use_container_width=True):
    if email_text.strip() == "":
        st.warning('⚠️ Please enter some text to analyze!')
    else:
        # Preprocess and predict
        transformed_text = vectorizer.transform([email_text])
        prediction = model.predict(transformed_text)[0]
        
        # Display result
        if prediction == 1:
            st.success("✅ This email is classified as **NOT SPAM**!", icon="✅")
        else:
            st.error("🚨 This email is classified as **SPAM**!", icon="🚨")
# Footer
st.markdown(
    "<hr style='border:1px solid #eee;'>",
    unsafe_allow_html=True
)
st.caption('Made with ❤️ using Streamlit')
