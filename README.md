#Email Spam Detection App

A machine learning web application that detects whether an email message is spam or not. Built using **Scikit-learn**, **Streamlit**, and a variety of classification algorithms.

## Overview

This project allows users to:
- **Sign up / log in** securely using hashed credentials (with `bcrypt`)
- **Paste email text** and classify it as **SPAM** or **NOT SPAM**
- Get an interactive and stylish UI powered by Streamlit and custom CSS

## Tech Stack

| Component | Technology |

| **Frontend** | Streamlit + HTML/CSS |
| **Backend** | Python + SQLite + bcrypt |
| **ML Models** | Logistic Regression, Naive Bayes, SVM, Random Forest, Gradient Boosting, KNN |
| **Deployment** | Streamlit Cloud |

---

## Project Structure
├── app.py # Streamlit main app
├── spam_model.pkl # Best performing ML model (SVM)
├── vectorizer.pkl # TF-IDF vectorizer
├── style.css # Custom styles for Streamlit app
├── users.db # SQLite DB for login/signup (auto-created if missing)
├── requirements.txt # Project dependencies
└── README.md # This file


## Model Building Summary

1. **Dataset**: SMS Spam Collection (`mail_data.csv`)
2. **Preprocessing**:
   - Filled missing values
   - Encoded `spam` as `0` and `ham` as `1`
3. **Feature Extraction**:
   - Used `TfidfVectorizer` to convert text into feature vectors
4. **Model Training**:
   - Trained 6 models and evaluated them using Accuracy, Precision, and Recall
   - Selected **Support Vector Machine (SVM)** as the best model

### Accuracy Results

| Model                  | Accuracy (%) |
|------------------------|--------------|
| Support Vector Machine | 95.40*Best*  |
| Random Forest          | 94.85        |
| Logistic Regression    | 93.70        |
| Naive Bayes            | 89.29        |
| Gradient Boosting      | 90.21        |
| K-Nearest Neighbors    | 75           |


## How to Run the App Locally

1. **Clone this repo**:

   ```bash
   git clone https://github.com/yourusername/email-spam-detector.git
   cd email-spam-detector
2. **Install Depandencies**
   pip install -r requirements.txt

3. **Run Streamlit**
   streamlit run app.py
