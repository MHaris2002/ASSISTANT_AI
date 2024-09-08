import speech_recognition as sr
import sys
from functions import say, takeCommand, process_query


if __name__ == '__main__':
    # Wait for wake word before starting
    r = sr.Recognizer()
    with sr.Microphone() as source:
        wake_word_detected = False
        print("Waiting...")
        while not wake_word_detected:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language="en-us")
                if 'hey assistant' in query.lower():
                    wake_word_detected = True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Error recognizing speech.")

    input_mode = None
    questions_count = 0
    max_questions = 5

    try:
        print("Welcome to your Assistant!")
        say("Welcome to your Assistant")
        while True:
            if questions_count == 0 or questions_count >= max_questions:
                say("Which mode would you like to adopt")
                print("Would you like to speak, type or exit? (Type 'speak', 'type', or 'exit')")
                input_mode = input().strip().lower()
                questions_count = 0

                if input_mode == 'exit':
                    say("Goodbye!")
                    break

                if input_mode not in ['speak', 'type', 'exit']:
                    say("Invalid mode. Please type 'speak', 'type', or 'exit'.")
                    continue

            if input_mode == 'speak':
                print("Listening...")
                user_input = takeCommand()
            elif input_mode == 'type':
                user_input = input("Please type your command: ")

            # Process the query
            if user_input:  # Only process if user_input is not empty
                process_query(user_input)
                questions_count += 1

    except KeyboardInterrupt:
        say("Goodbye!")
        sys.exit()
