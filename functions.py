import os
import webbrowser
import pyttsx3  # For text-to-speech on Windows
import datetime
from groq import Groq
from googlesearch import search
from config import apikey
import speech_recognition as sr
import signal
import sys
import shutil

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def set_female_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Zira" in voice.name:  # Look for the Zira voice
            engine.setProperty('voice', voice.id)
            break

# Set the voice to female at the start
set_female_voice()

def say(text):
    engine.say(text)  # Use pyttsx3 to speak the text
    engine.runAndWait()  # Ensure speaking happens

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")
            print(f"User said: {query}")
            if 'stop' in query.lower():  # Stop if the user says "stop"
                say("Assistant stopping as per user request")
                sys.exit()  # Exit the assistant
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error with the request.")
            return ""


# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

#If there is an issue setting up api key in environment variables, you can do like this as well
'''apikey='YOUR_API_KEY'
client = Groq(api_key=apikey)'''

# Folder and file tracking variables
responses_dir = "Assistant_Responses"
response_list = []
file_path = None  # Track the current file path
file_created = False  # Flag to check if file has been created

# Create folder if it doesn't exist
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

def create_new_file(file_name):
    global file_path
    file_path = os.path.join(responses_dir, f"{file_name}.txt")


def save_responses_to_file():
    global response_list, file_path

    with open(file_path, "a") as file:  # Use "a" mode to append
        for idx, item in enumerate(response_list):
            file.write(f"Question : {item['question']}\n")
            file.write(f"Response : {item['response']}\n\n")

    response_list.clear()  # Clear the list after saving


def delete_chat_history():
    global response_list, file_created, responses_dir
    # Clear the in-memory response list
    response_list.clear()

    # Delete all text files in the Assistant_Responses directory
    if os.path.exists(responses_dir):
        shutil.rmtree(responses_dir)
        os.makedirs(responses_dir)  # Recreate the directory after deletion
    file_created = False  # Reset the file creation flag


def get_first_google_result(query):
    try:
        search_results = search(query, num_results=10)
        search_results_list = list(search_results)
        if search_results_list:
            return search_results_list[0]
        else:
            return None
    except:
        return None


def process_query(query):
    global response_list, file_created

    if "search for" in query.lower():
        search_query = query.lower().replace("search for", "").strip()
        result_url = get_first_google_result(search_query)
        if result_url:
            print(f"Opening search result for {search_query}...")
            say(f"Opening search result for {search_query}...")
            webbrowser.open(result_url)
        else:
            print("Sorry, I couldn't find any results.")
            say("Sorry, I couldn't find any results.")
        response = f"Opened search result for {search_query}"

    elif "the time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        response = f"The time is {hour} hours and {min} minutes"
        print(response)
        say(response)

    elif "reset chat" in query.lower():
        response = "Chat history has been reset."
        print(response)
        say(response)

    elif "delete history" in query.lower():
        delete_chat_history()
        response = "All chat history and responses have been deleted."
        print(response)
        say(response)

    else:
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "user", "content": query}
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            response_text = ""
            for chunk in completion:
                if hasattr(chunk, 'choices') and chunk.choices:
                    response_text += chunk.choices[0].delta.content or ""

            if not response_text:
                response_text = "Sorry, I didn't get that. Can you repeat again?"

            response = response_text
            print(f"Response: {response}")
            say(response)
        except KeyboardInterrupt:
            sys.exit()

    # Append the question and response to the list
    response_list.append({"question": query, "response": response})

    # Create a new file with the first response if not created yet
    if not file_created and response_list:
        first_response = response_list[0]['response'].strip().replace(" ", "_").replace("/", "_").replace("\\", "_")
        create_new_file(first_response[:50])  # Limit filename length to avoid issues with long names
        file_created = True

    # Save responses to file
    save_responses_to_file()


def signal_handler(sig, frame):
    say("Goodbye!")  # Say goodbye before exiting
    sys.exit()


# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)