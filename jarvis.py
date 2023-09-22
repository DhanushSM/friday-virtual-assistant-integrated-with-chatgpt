import openai
import pyttsx3
import speech_recognition as sr
import random
import os
import time
from api import api_key  # Make sure to replace 'api_key' with your actual OpenAI API key

# Configuration
model_id = "gpt-3.5-turbo"
openai.api_key = api_key
# Replace with your OpenAI API key

# Initialize text-to-speech engine with a female voice
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# Select a female voice (you may need to check the voice index)
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if "female" in voice.name.lower():
        female_voice = voice
        break

if female_voice:
    engine.setProperty('voice', female_voice.id)
else:
    print("No female voice found. Using the default voice.")

interaction_counter = 0

trigger_word = "Friday"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return ""

def chat_with_gpt(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    print('Total tokens consumed: {0}'.format(api_usage['total_tokens']))
    response_text = response.choices[0].message.content.strip()
    return response_text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def activate_assistant():
    starting_chat_phrases=["Yes, sir. How may I assist you?",
                           "Yes, sir. What can I do for you?",
                           "Friday here, ready to assist you.",
                           "Yes, sir. What's on your mind?",
                           "Friday ready to assist, how can I help?",
                           "On your command, sir. How may I assist you?",
                           "Yes, sir. How may I be of assistance to you right now?",
                           "Yes, boss. I'm here to help. What can I do for you?",
                           "On your word, ready to assist you, sir?",
                           "Yes, sir. What's on your mind?"]

    continued_chat_phrases = ["Yes, sir", "Yes, boss", "On your command, sir", "On your lead"]

    random_chat = random.choice(starting_chat_phrases) if interaction_counter == 1 else random.choice(continued_chat_phrases)
    return random_chat

def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")

conversation = []
conversation.append({'role': 'user', 'content': 'Please, act like Friday AI from Iron Man, make a 1 sentence introduction yourself without saying something that sounds like chat is already'})
conversation = chat_with_gpt(conversation)

def listen_for_trigger():
    global conversation, interaction_counter, last_interaction_time

    while True:
        print("Say 'Friday' to start...")
        user_input = recognize_speech()
        if user_input and trigger_word.lower() in user_input.lower():
            interaction_counter += 1
            filename = "input.wav"
            ready_to_work = activate_assistant()
            speak_text(ready_to_work)
            print(ready_to_work)
            last_interaction_time = time.time()

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

            text = transcribe_audio_to_text(filename)

            if text:
                print(f"You said: {text}")
                append_to_log(f"You: {text}\n")
                print(f"Assistant says: {conversation}")
                prompt = text
                conversation.append({'role': 'user', 'content': prompt})
                assistant_response = chat_with_gpt(conversation)
                print(f"Assistant: {assistant_response}")
                append_to_log(f"Assistant: {assistant_response}\n")
                speak_text(assistant_response)

        # Check if there has been no input for a certain period (e.g., 2 minutes)
        if time.time() - last_interaction_time > 120:  # 120 seconds = 2 minutes
            print("Sir, are you there?")
            speak_text("Sir, are you there?")
            response = recognize_speech()
            if response and "yes" in response.lower():
                last_interaction_time = time.time()
                print("Great! How can I assist you?")
                speak_text("Great! How can I assist you?")
            else:
                print("No response. Exiting.")
                break

# Initialize the last_interaction_time variable
last_interaction_time = time.time()

# Call the function to listen for the trigger word
listen_for_trigger()
