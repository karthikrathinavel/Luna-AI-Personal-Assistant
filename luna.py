import os
import datetime 
import pyttsx3
import sounddevice as sd
import speech_recognition as sr
from google import genai
from dotenv import load_dotenv
import webbrowser

load_dotenv()

# 1. Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Details: {e}")
    exit(1)

assistant_name = "Luna"

system_instruction = f"You are a highly efficient, witty personal assistant named {assistant_name}. Keep your responses concise, conversational, and avoid using complex markdown formatting."

def get_current_time() -> str:
    """Returns the current local time on the user's computer."""
    now = datetime.datetime.now()
    print("[System: Luna checked the time]") # Just so you can see it working!
    return now.strftime("%I:%M %p")

def get_current_date() -> str:
    """Returns the current local date on the user's computer."""
    now = datetime.datetime.now()
    print("[System: Luna checked the date]")
    return now.strftime("%B %d, %Y")

def open_website(website_name: str) -> str:
    """Opens a popular website in the default browser based on the name provided."""
    print(f"[System: Luna is opening {website_name}]")
    url = f"https://www.{website_name.lower()}.com"
    webbrowser.open(url)
    return f"Successfully opened {website_name}."

# 2. Text-to-Speech (TTS) Engine
def speak(text):
    print(f"{assistant_name}: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if len(voices) > 0:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    
    engine.say(text)
    try:
        engine.runAndWait()
    except Exception:
        pass
    engine.stop()

# 3. Custom Speech-to-Text (STT)
def listen():
    try:
        device_info = sd.query_devices(kind='input')
        sample_rate = int(device_info['default_samplerate'])
    except Exception:
        sample_rate = 16000

    print("\n[Listening for 5 seconds... Speak now!]")
    duration = 5
    audio_bytes = bytearray()

    def callback(indata, frames, time, status):
        audio_bytes.extend(bytes(indata))

    try:
        with sd.RawInputStream(samplerate=sample_rate, channels=1, dtype='int16', callback=callback):
            sd.sleep(int(duration * 1000))
        
        print("[Processing...]")
        audio_data = sr.AudioData(bytes(audio_bytes), sample_rate, 2)
        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("[Sorry, I didn't catch that.]")
        return None
    except Exception as e:
        print(f"[Audio error: {e}]")
        return None
    
# 4. Main Assistant Loop
try:
    chat_session = client.chats.create(
        model='gemini-3.5-flash',
        config={
            "system_instruction": system_instruction,
            "tools": [get_current_time, get_current_date, open_website] # <-- NEW: We handed Luna the tools!
        }
    )
except Exception as e:
    print(f"Failed to start chat session: {e}")
    exit(1)

speak(f"{assistant_name} is online. Say shut down to turn me off")

while True:
    user_input = listen()

    if user_input is None:
        continue

    if "shut down" in user_input.lower() or "exit" in user_input.lower():
        speak("Powering down. Goodbye!")
        break

    try:
        response = chat_session.send_message(user_input)

        clean_response = response.text.replace('*', '').replace('#', '')
        speak(clean_response)
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "Quota" in error_message:
            speak("I'm hitting my API rate limit. Please give me about 30 seconds to catch my breath.")
        else:
            speak("I encountered an error connecting to my core servers.")
            print(f"Details: {e}")
