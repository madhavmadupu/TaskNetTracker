import streamlit as st
import pandas as pd
from git import Repo
from datetime import datetime
import pytz
import subprocess

# Function to load existing data or create a new DataFrame
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "task", "task_description", "task_duration", "importance", "interest",
            "type", "preferred_shift", "day_of_week", "month", "year",
            "time_of_day", "weekday_weekend", "is_holiday", "weather_conditions",
            "energy_level", "mood", "location"
        ])
    return df

# Function to save data to CSV
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Function to get Indian date and time
def get_indian_datetime():
    tz = pytz.timezone('Asia/Kolkata')  # Indian Standard Time (IST)
    indian_datetime = datetime.now(tz)
    return indian_datetime

# Main Streamlit app
def main():
    st.title("Task Recommendation Data Entry")

    # Load existing data or create a new DataFrame
    data_file_path = "./task_data.csv"
    df = load_data(data_file_path)

    # Task input form
    col1, col2 = st.columns(2)

    with col1:
        task = st.text_input("Task")
        task_description = st.text_input("Task Description")
        preferred_shift = st.selectbox("Preferred Shift", ["Morning", "Afternoon", "Evening"])
        importance = st.slider("Importance", min_value=1, max_value=10, value=5)

    with col2:
        task_type = st.selectbox("Task Type", ["Work", "Health", "Personal", "Other"])
        task_duration = st.number_input("Task Duration (hours)", min_value=0.1, step=0.1)
        weather_conditions = st.text_input("Weather Conditions")
        interest = st.slider("Interest", min_value=1, max_value=10, value=5)

    st.text("")  # Add some space
    st.subheader("Optional Details")

    col3, col4, col5 = st.columns(3)

    with col3:
        weekday_weekend = st.radio("Weekday/Weekend", ["Weekday", "Weekend"])
        is_holiday = st.checkbox("Is Holiday?")

    with col4:
        energy_level = st.slider("Energy Level", min_value=1, max_value=10, value=5)

    with col5:
        mood = st.selectbox("Mood", ["Neutral", "Happy", "Stressed", "Relaxed"])
        location = st.selectbox("Location", ["Home", "College", "Outdoors", "Other"])

    # Save data on button click
    if st.button("Save Task"):
        indian_datetime = get_indian_datetime()

        new_row = {
            "task": task, "task_description": task_description, "task_duration": task_duration,
            "importance": importance, "interest": interest, "type": task_type,
            "preferred_shift": preferred_shift, "day_of_week": indian_datetime.weekday() + 1,
            "month": indian_datetime.month, "year": indian_datetime.year,"weekday_weekend": weekday_weekend,
            "is_holiday": is_holiday, "weather_conditions": weather_conditions,
            "energy_level": energy_level, "mood": mood, "location": location
        }

        df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True, sort=False)
        save_data(df, data_file_path)
        st.success("Task saved successfully!")


    # Display the current data
    st.subheader("Current Data")
    st.dataframe(df)

if __name__=="__main__":
    st.set_page_config(page_title="TaskNet", page_icon="📅")
    main()