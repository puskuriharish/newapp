import streamlit as st
import datetime
import requests
import os
from dotenv import load_dotenv

# --- Load API Key from .env ---
load_dotenv()  # Load environment variables from .env
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Get API key securely
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# --- Custom CSS Styles ---
st.markdown(
    """
    <style>
    body {
        background-color: #eaeff1;
    }
    .stApp {
        background: linear-gradient(135deg, #4f8cff, #1e3c72);
        padding-top: 20px;
    }
    .main-container {
        background-color: #ffffff10;
        padding: 30px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        width: 70%;
        margin: 20px auto;
        backdrop-filter: blur(12px);
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #fff;
        text-align: center;
        padding-bottom: 10px;
    }
    .info-text {
        font-size: 18px;
        color: #ddd;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTextInput, .stTextArea, .stDateInput, .stRadio > div {
        border-radius: 8px;
        padding: 10px;
        background-color: #ffffff20;
        color: #fff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .budget-btn {
        margin: 5px 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .budget-btn:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Helper Function to Get Response from Together AI ---
def get_together_response(prompt):
    """Fetches a response from Together AI based on the user prompt."""
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",  # Choose appropriate model
        "messages": [
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    
    response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Streamlit UI ---
st.markdown("<div class='main-title'>🌍 AI-Powered Trip Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='info-text'>Plan your perfect trip with personalized recommendations powered by Together AI!</div>", unsafe_allow_html=True)

# --- Main Container for Neat UI ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Collecting User Inputs with Forms
with st.form("trip_form", clear_on_submit=True):
    destination = st.text_input("📍 Where are you traveling to?")
    start_date = st.date_input("📅 Start Date", datetime.date.today())
    end_date = st.date_input("📅 End Date", datetime.date.today())
    interests = st.text_area("🎯 What activities or interests do you have?")
    
    # --- Budget Options as Buttons ---
    st.markdown("💸 **Select Your Budget:**")
    budget_options = ["Budget", "Moderate", "Luxury"]
    budget_choice = st.radio(
        "", budget_options, horizontal=True
    )

    submit_button = st.form_submit_button("✨ Get My Itinerary")

# --- Close Main Container ---
st.markdown("</div>", unsafe_allow_html=True)

# --- Validate and Process User Input ---
if submit_button:
    if destination and start_date and end_date:
        days = (end_date - start_date).days + 1

        # --- Build User Context Prompt ---
        user_input_prompt = f"Generate a {days}-day itinerary for a trip to {destination} with a {budget_choice.lower()} budget. "
        user_input_prompt += f"Interests include {interests}. "
        user_input_prompt += f"Provide a mix of popular attractions and hidden gems."

        # --- Get Response from Together AI ---
        itinerary = get_together_response(user_input_prompt)
        
        # --- Display Itinerary ---
        st.subheader("📅 Your Personalized Itinerary")
        st.write(itinerary)
    else:
        st.warning("⚠️ Please fill in all required fields!")
