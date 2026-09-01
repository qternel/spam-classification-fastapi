import os

import requests
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

api_address = os.getenv("API_ADDRESS")

st.title("Spam message classification")
message = st.text_input("Message to classify", key="message")

if st.button("Classify"):
    response = requests.get(
        f"http://{api_address}:8000/classify", params={"text": message}
    )

    st.text("Spam message" if response.json()["is_spam"] else "Not a spam message")

st.title("\nMisclassification collection\n")

test_message = st.text_input("Message to classify", key="test_message")
label = st.checkbox("Is Spam")

if st.button("Collect Misclassification"):
    response = requests.post(
        f"http://{api_address}:8000/collect_misclassification",
        json={"text": test_message, "true_label": label},
    )

if st.button("Get Misclassifications"):
    lst = requests.get(f"http://{api_address}:8000/get_misclassifications").json()
    st.write(lst)
