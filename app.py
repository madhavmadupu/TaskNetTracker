import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Function to load existing data or create a new DataFrame
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        data = pd.DataFrame(columns=[
            "task", "task_description", "task_duration", "importance", "interest",
            "type", "preferred_shift", "day_of_week", "month", "year",
            "time_of_day", "weekday_weekend", "is_holiday", "weather_conditions",
            "energy_level", "mood", "location"
        ])
    return data

# Function to save data to CSV
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# Function to get Indian date and time
def get_indian_datetime():
    tz = pytz.timezone('Asia/Kolkata')  # Indian Standard Time (IST)
    indian_datetime = datetime.now(tz)
    return indian_datetime

# Main Streamlit app
def main():
    st.title("Task Recommendation Data Entry")

    # Load existing data or create a new DataFrame
    data_file_path = "task_data.csv"
    data = load_data(data_file_path)

    # Task input form
    col1, col2 = st.columns(2)

    with col1:
        task = st.text_input("Task")
        task_description = st.text_input("Task Description")
        task_duration = st.number_input("Task Duration (hours)", min_value=0.1, step=0.1)
        importance = st.slider("Importance", 1, 10)
        interest = st.slider("Interest", 1, 10)

    with col2:
        task_type = st.selectbox("Task Type", ["Work", "Health", "Personal", "Other"])
        preferred_shift = st.selectbox("Preferred Shift", ["Morning", "Afternoon", "Evening"])

    # Save data on button click
    if st.button("Save Task"):
        indian_datetime = get_indian_datetime()

        new_row = {
            "task": task, "task_description": task_description, "task_duration": task_duration,
            "importance": importance, "interest": interest, "type": task_type,
            "preferred_shift": preferred_shift, "day_of_week": indian_datetime.weekday() + 1,
            "month": indian_datetime.month, "year": indian_datetime.year,
            "time_of_day": time_of_day, "weekday_weekend": weekday_weekend,
            "is_holiday": is_holiday, "weather_conditions": weather_conditions,
            "energy_level": energy_level, "mood": mood, "location": location
        }

        data = data.append(new_row, ignore_index=True)
        save_data(data, data_file_path)
        st.success("Task saved successfully!")
        
    st.text("")  # Add some space
    st.subheader("Optional Details")

    col3, col4, col5 = st.columns(3)

    with col3:
        time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])
        weekday_weekend = st.radio("Weekday/Weekend", ["Weekday", "Weekend"])
        is_holiday = st.checkbox("Is Holiday?")

    with col4:
        weather_conditions = st.text_input("Weather Conditions")
        energy_level = st.slider("Energy Level", 1, 10)

    with col5:
        mood = st.selectbox("Mood", ["Happy", "Neutral", "Stressed", "Relaxed"])
        location = st.selectbox("Location", ["Home", "Office", "Outdoors", "Other"])


    # Display the current data
    st.subheader("Current Data")
    st.dataframe(data)

if __name__ == "__main__":
    main()
