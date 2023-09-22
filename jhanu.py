import openai
import pyttsx3
import speech_recognition as sr
import random
import os
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
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def activate_assistant():
    starting_chat_phrases=["Yes, princess, how may I assist you?",
                           "Of course, my angel, what can I do for you?",
                           "Hello, my dear princess. How can I help you today?",
                           "Yes, my angel, what's on your mind?",
                           "Ready to assist, my princess. What can I do for you?",
                           "On your command, my angel. How may I help you today?",
                           "Yes, my dear princess, how may I be of assistance to you right now?",
                           "Yes, my angel. I'm here to help. What can I do for you?",
                           "On your word, my princess. Ready to assist you.",
                           "Yes, my angel. What's on your mind?"]

    continued_chat_phrases = ["Yes, princess", "Yes, my angel", "On your command, my princess", "On your lead, my angel"]

    random_chat = random.choice(starting_chat_phrases) if interaction_counter == 1 else random.choice(continued_chat_phrases)
    return random_chat

def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")

conversation = []
conversation.append({'role':'user','content':'please, act like a friendly AI and make a 1 sentence introduction about yourself without using chat-related terms'})
conversation = chat_with_gpt(conversation)
print('{0}:{1}\n'.format(conversation[-1]['role'].strip(),conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())
keyword = "Friday"  # Your activation keyword

def listen_for_keyword():
    global conversation, interaction_counter  # Declare conversation and interaction_counter as global variables
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=10)  # Timeout set to 10 seconds

        try:
            transcription = recognizer.recognize_google(audio)

            if keyword.lower() in transcription.lower():
                interaction_counter += 1
                filename = "input.wav"
                ready_to_work = activate_assistant()
                speak_text(ready_to_work)  # Corrected variable name here
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
                    print(f"Friday says: {conversation}")
                    prompt = text
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = chat_with_gpt(conversation)  # Moved conversation assignment here
                    print("{0}: {1}\n".format(conversation[-1]['role'].strip(), conversation[-1]['content']))
                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")
                    speak_text(conversation[-1]["content"].strip())
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Call the function to listen for the keyword
while True:
    print("Say 'Friday' to start...")
    listen_for_keyword()

    # After the keyword is detected, capture user input using recognize_speech
    user_input = recognize_speech()
    if user_input:
        print(f"You said: {user_input}")
        append_to_log(f"You: {user_input}\n")
        # Continue with the conversation, if needed
