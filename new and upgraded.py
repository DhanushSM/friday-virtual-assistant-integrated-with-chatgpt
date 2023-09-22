import openai
import pyttsx3
import speech_recognition as sr
import random
import os
import webbrowser
import subprocess
import datetime
import time

# Make sure to import your API key from your API file
from api import api_key

# Configuration
model_id = "gpt-3.5-turbo"
openai.api_key = api_key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

interaction_counter = 0
last_interaction_time = time.time()  # Initialize last interaction time


def recognize_speech(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return None

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
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def activate_assistant():
    starting_chat_phrases = [
        "Yes sir, how may I assist you?",
        "Yes sir, what can I do for you?",
        "Friday here, how can I help you today?",
        "Yes sir, what's on your mind?",
        "Friday ready to assist, what can I do for you?",
        "On your command, sir. How may I help you today?",
        "Yes sir, how may I be of assistance to you right now?",
        "Yes boss, I'm here to help. What can I do for you?",
        "On your word, ready to assist you sir?",
        "Yes sir, what's on your mind?"
    ]

    continued_chat_phrases = ["Yes, sir", "Yes, boss", "On your command, sir", "On your lead"]

    random_chat = random.choice(starting_chat_phrases) if interaction_counter == 1 else random.choice(
        continued_chat_phrases)
    return random_chat


def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")


conversation = []
conversation.append({'role': 'user',
                     'content': 'please, act like a friendly AI and make a 1 sentence introduction about yourself without using chat-related terms'})
conversation = chat_with_gpt(conversation)
print('{0}:{1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())
keyword = "Friday"  # Your activation keyword


def listen_for_keyword():
    global conversation, interaction_counter, last_interaction_time
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=10)

        try:
            transcription = recognizer.recognize_google(audio)

            if keyword.lower() in transcription.lower():
                interaction_counter += 1
                filename = "input.wav"
                ready_to_work = activate_assistant()
                speak_text(ready_to_work)
                print(ready_to_work)

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

                    if "open chrome" in text:
                        speak_text("Opening Google Chrome for you, Boss.")
                        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
                        subprocess.Popen([chrome_path])
                    elif "open youtube" in text:
                        speak_text("Opening YouTube for you, Boss.")
                        url = "https://www.youtube.com"
                        subprocess.Popen(["start", "chrome", url], shell=True)

                    print(f"Friday says: {conversation}")
                    prompt = text
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = chat_with_gpt(conversation)
                    print("{0}: {1}\n".format(conversation[-1]['role'].strip(), conversation[-1]['content']))
                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")
                    speak_text(conversation[-1]["content"].strip())

                    # Reset the last interaction time upon user interaction
                    last_interaction_time = time.time()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


# Call the function to listen for the keyword
try:
    while True:
        if time.time() - last_interaction_time > 120:
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

        print("Say 'Friday' to start...")
        listen_for_keyword()
except KeyboardInterrupt:
    print("Exiting...")
import openai
import pyttsx3
import speech_recognition as sr
import random
import os
import webbrowser
import subprocess
import datetime
import time

# Make sure to import your API key from your API file
from api import api_key

# Configuration
model_id = "gpt-3.5-turbo"
openai.api_key = api_key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

interaction_counter = 0
last_interaction_time = time.time()  # Initialize last interaction time


def recognize_speech(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return None

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
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def activate_assistant():
    starting_chat_phrases = [
        "Yes sir, how may I assist you?",
        "Yes sir, what can I do for you?",
        "Friday here, how can I help you today?",
        "Yes sir, what's on your mind?",
        "Friday ready to assist, what can I do for you?",
        "On your command, sir. How may I help you today?",
        "Yes sir, how may I be of assistance to you right now?",
        "Yes boss, I'm here to help. What can I do for you?",
        "On your word, ready to assist you sir?",
        "Yes sir, what's on your mind?"
    ]

    continued_chat_phrases = ["Yes, sir", "Yes, boss", "On your command, sir", "On your lead"]

    random_chat = random.choice(starting_chat_phrases) if interaction_counter == 1 else random.choice(
        continued_chat_phrases)
    return random_chat


def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")


conversation = []
conversation.append({'role': 'user',
                     'content': 'please, act like a friendly AI and make a 1 sentence introduction about yourself without using chat-related terms'})
conversation = chat_with_gpt(conversation)
print('{0}:{1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())
keyword = "Friday"  # Your activation keyword


def listen_for_keyword():
    global conversation, interaction_counter, last_interaction_time
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=10)

        try:
            transcription = recognizer.recognize_google(audio)

            if keyword.lower() in transcription.lower():
                interaction_counter += 1
                filename = "input.wav"
                ready_to_work = activate_assistant()
                speak_text(ready_to_work)
                print(ready_to_work)

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

                    if "open chrome" in text:
                        speak_text("Opening Google Chrome for you, Boss.")
                        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
                        subprocess.Popen([chrome_path])
                    elif "open youtube" in text:
                        speak_text("Opening YouTube for you, Boss.")
                        url = "https://www.youtube.com"
                        subprocess.Popen(["start", "chrome", url], shell=True)

                    print(f"Friday says: {conversation}")
                    prompt = text
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = chat_with_gpt(conversation)
                    print("{0}: {1}\n".format(conversation[-1]['role'].strip(), conversation[-1]['content']))
                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")
                    speak_text(conversation[-1]["content"].strip())

                    # Reset the last interaction time upon user interaction
                    last_interaction_time = time.time()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


# Call the function to listen for the keyword
try:
    while True:
        if time.time() - last_interaction_time > 120:
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

        print("Say 'Friday' to start...")
        listen_for_keyword()
except KeyboardInterrupt:
    print("Exiting...")
