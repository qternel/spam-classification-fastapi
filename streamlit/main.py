import os

import requests
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

api_address = os.getenv("API_ADDRESS")

st.title("Spam message classification")
message = st.text_input("Message to classify")

if st.button("Classify"):
    response = requests.get(
        f"http://{api_address}:8000/classify", params={"text": message}
    )

    st.text("Spam message" if response.json()["is_spam"] else "Not a spam message")
