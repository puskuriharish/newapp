import streamlit as st
import openai
import os
import json

# Load prompts from JSON file
def load_prompts():
    with open("prompts.json", "r") as file:
        return json.load(file)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load prompts
prompts = load_prompts()

# App title and intro
st.title("✈️ AI Travel Planner")
st.write("Plan your next adventure with personalized itineraries!")

# Collect user input
budget = st.selectbox("What's your budget?", ["Low", "Moderate", "High"])
duration = st.number_input("How many days is your trip?", min_value=1, max_value=30, step=1)
destination = st.text_input("Where are you traveling to?")
start_location = st.text_input("Where are you starting from?")
purpose = st.selectbox("What's the purpose of your trip?", ["Leisure", "Adventure", "Work", "Honeymoon", "Other"])
interests = st.text_area("Any specific preferences or interests? (e.g., food, culture, adventure)")

# Generate itinerary when user clicks
if st.button("Generate Itinerary"):
    if destination and duration:
        # Prepare user inputs
        user_input = {
            "destination": destination,
            "duration": duration,
            "budget": budget,
            "purpose": purpose,
            "interests": interests
        }
        
        # Build prompt
        prompt = prompts["final_itinerary_prompt"].format(**user_input)
        
        # Generate response
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=500
        )
        
        # Display itinerary
        st.subheader("Your Personalized Itinerary:")
        st.write(response.choices[0].text.strip())
    else:
        st.warning("Please provide at least the destination and duration.")
