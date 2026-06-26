import os
import uuid
import pandas as pd
import speech_recognition as sr
from groq import Groq
from gtts import gTTS
import playsound
from datetime import datetime
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv() # This loads the variables from the .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

CSV_FILE = "patient_data1.csv"

def speak(text):
    """Converts text to speech and plays it back."""
    print(f"🔊 AI: {text}")
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        # Use absolute path for playsound stability
        full_path = os.path.abspath(filename)
        playsound.playsound(full_path)
    except Exception as e:
        print(f"Audio Playback Error: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# def get_ai_response(user_query):
#     """Filters CSV data and asks Groq AI for an answer."""
#     try:
#         # 1. Load the CSV
#         df = pd.read_csv(CSV_FILE)

#         # 2. Convert your custom '20260312200547' format to readable dates
#         # This handles the YYYYMMDDHHMMSS format
#         df['parsed_time'] = pd.to_datetime(df['Timestamp'], format='%Y%m%d%H%M%S', errors='coerce')

#         # 3. Filtering Logic (To stay under Groq's 6000 token limit)
#         # We find the most recent date in your CSV and only send that day's data
#         latest_date = df['parsed_time'].max().date()
#         filtered_df = df[df['parsed_time'].dt.date == latest_date]

#         # Take only the last 30 entries of that day to be safe
#         context_data = filtered_df.tail(30).drop(columns=['parsed_time']).to_string(index=False)

#         # 4. Prompt the AI
#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "system", 
#                     "content": (
#                         f"You are a helpful health assistant. Today's date is {datetime.now().date()}. "
#                         "The user's health logs are provided below. "
#                         "Identify the time the user is asking about and provide the HR, SpO2, and Temp. "
#                         "If the exact time isn't there, use the closest match. Keep it conversational."
#                     )
#                 },
#                 {
#                     "role": "user", 
#                     "content": f"Health Logs for {latest_date}:\n{context_data}\n\nUser Question: {user_query}"
#                 }
#             ],
#             temperature=0.1
#         )
#         return completion.choices[0].message.content

#     except Exception as e:
#         return f"I encountered an error processing your data: {str(e)}"

# def get_ai_response(user_query):
#     try:
#         df = pd.read_csv(CSV_FILE)
#         df['parsed_time'] = pd.to_datetime(df['Timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
        
#         latest_date = df['parsed_time'].max().date()
#         filtered_df = df[df['parsed_time'].dt.date == latest_date].copy()

#         # --- IMPROVEMENT: Create a readable time column ---
#         filtered_df['Readable_Time'] = filtered_df['parsed_time'].dt.strftime('%H:%M (%I:%M %p)')
        
#         # Only send relevant columns to save tokens and improve focus
#         context_data = filtered_df[['Readable_Time', 'HR', 'SpO2', 'Temp']].tail(30).to_string(index=False)

#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "system", 
#                     "content": (
#                         f"You are a medical data assistant. Today is {datetime.now().date()}. "
#                         "Below is a table of health logs. The 'Readable_Time' column shows 24h and 12h formats. "
#                         "When a user asks for a time, find the row that matches that time best. "
#                         "Report the HR (Heart Rate), SpO2 (Oxygen), and Temp (Temperature) clearly."
#                     )
#                 },
#                 {
#                     "role": "user", 
#                     "content": f"Data Logs:\n{context_data}\n\nUser Question: {user_query}"
#                 }
#             ],
#             temperature=0.1 # Keep temperature low for factual accuracy
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"Error: {str(e)}"

def get_ai_response(user_query):
    try:
        df = pd.read_csv(CSV_FILE)

        # Auto parse timestamps
        df['parsed_time'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # Remove invalid rows
        df = df.dropna(subset=['parsed_time'])

        if df.empty:
            return "No valid data found in the CSV."

        # Create readable time
        df['Readable_Time'] = df['parsed_time'].dt.strftime('%H:%M')

        print(df[['Readable_Time', 'HR', 'SpO2', 'Temp', 'BP']].tail())

        # Extract time from user query
        import re

        match = re.search(r'(\d{1,2})[: ]?(\d{2})', user_query)

        if not match:
            return "I could not understand the time."

        hour = int(match.group(1))
        minute = int(match.group(2))

        target_time = f"{hour:02}:{minute:02}"

        # Find matching row
        matched_row = df[df['Readable_Time'] == target_time]

        if matched_row.empty:
            return f"No data found for {target_time}"

        row = matched_row.iloc[0]

        return (
            f"At {target_time}, "
            f"heart rate was {row['HR']}, "
            f"oxygen level was {row['SpO2']} percent, "
            f"temperature was {row['Temp']} degree Celsius, "
            f"and blood pressure was {row['BP']}."
        )

    except Exception as e:
        return f"Error: {str(e)}"

def start_voice_assistant():
    """Main loop for listening and responding."""
    recognizer = sr.Recognizer()
    
    # Simple check if CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found!")
        return

    speak("I am listening. Which time would you like me to check?")

    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # 5 second limit to stop it from hanging
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        print("🧠 Processing voice...")
        user_input = recognizer.recognize_google(audio)
        print(f"👤 You: {user_input}")

        # Get reasoning from Groq
        ai_answer = get_ai_response(user_input)
        
        # Speak the result
        speak(ai_answer)

    except sr.WaitTimeoutError:
        speak("I didn't hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("I'm sorry, I couldn't understand that. Could you repeat the time?")
    except Exception as e:
        print(f"System Error: {e}")
        speak("Sorry, I ran into a technical problem.")

if __name__ == "__main__":
    # Ensure terminal output is visible immediately
    start_voice_assistant()