import os
import datetime
import webbrowser
import logging
import nltk
import openai
import pyttsx3
import requests
import threading
import subprocess
import speech_recognition as sr
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from functools import cache
import google.generativeai as genai
nltk.download('vader_lexicon')
@cache

def cypher():
    # Set up text-to-speech engine
    global now
    engine = pyttsx3.init()

    # Set up speech recognition
    recognizer = sr.Recognizer()

    # Set up OpenAI API
    openai.api_key = ""

    # Set up GeminiApi
    genai.configure(api_key="")
    model = genai.GenerativeModel('gemini-pro')


    # Enter standby mode
    standby = True

    # Continuously listen for voice commands
    while standby:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            # Convert speech to text
            command = recognizer.recognize_google(audio).lower()
            # Wake up cypher
            now = datetime.datetime.now()
            if "tomato" in command:
                # Greet the user based on the time of day
                if now.hour < 12:
                    speak("Good morning sir")
                    print("Good morning sir")
                elif now.hour < 18:
                    speak("Good afternoon sir")
                    print("Good afternoon sir")
                else:
                    speak("Good evening sir")
                    print("Good evening sir")
                standby = False

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")

    # Process voice commands
    while not standby:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Convert speech to text
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")

            # Turn off cypher
            if "leave" in command or "sleep" in command or "fuck off" in command:
                speak("Do you want me to shutdown this system as well ?")
                print("Do you want me to shutdown this system as well ?")
                if "yes" in command:
                    speak("Initiating System Shut down.")
                    print("Initiating System Shut down.")
                    os.system("shutdown /s /t 1")
                else:
                    speak("cypher Ai assistant system shutdown.")
                    print("cypher Ai assistant system shutdown.")

            # StandBy mode
            elif "thank you tomato" in command or "thank you" in command:
                speak("You're welcome, sir.")
                print("You're welcome, sir.")
                cypher()

            # Shut Down System
            elif "shutdown" in command:
                speak("Initiating System Shut down.")
                print("Initiating System Shut down.")
                os.system("shutdown /s /t 1")

            # Restart System
            elif "restart" in command:
                speak("Initiating System Restart.")
                print("Initiating System Restart.")
                os.system("shutdown /r /t 1")

            # code generation
            elif "write a code" in command or "code for" in command or "code" in command:
                print("generating code./.")
                speak("generating code")
                chat = model.start_chat(history=[])
                response = chat.send_message(f"{command}")
                print(response.text)
                cmd = chat.send_message("Explain the above code.")
                print(cmd.text)
                speak(cmd.text)

            # Virus Scan
            elif "scan downloads" in command:
                speak("Scanning Downloads folder for viruses.")
                print("Scanning Downloads folder for viruses.")
                scan("Downloads")

            # Get the current time
            elif "what time is it" in command or "What is the time" in command:
                now = datetime.datetime.now()
                speak(f"The time is {now.strftime('%I:%M %p')}")
                print(f"The time is {now.strftime('%I:%M %p')}")

            # Get the current date
            elif "what's today's date" in command or "what's the date today" in command:
                now = datetime.datetime.now()
                speak(f"Today is {now.strftime('%B %d, %Y')}")
                print(f"Today is {now.strftime('%B %d, %Y')}")

            # Search the web
            elif "search" in command or "google" in command:
                query = command.replace("search", "")
                speak(f"Searching for {query} on Google.")
                print(f"Searching for {query} on Google.")
                search_url = "https://www.google.com/search?q=" + query
                webbrowser.open(search_url)

            # Answer a question
            elif "what" in command or "who" in command or "where" in command or "when" in command or "how" in command:
                print("Let me look that up for you.")
                question = command
                search_results = google_search(question)
                # webbrowser.open(f"https://www.google.com/search?q={question}")
                speak(search_results)
                print(search_results)

                # Open Youtube
            elif "open youtube" in command:
                speak("Opening youtube")
                print("Opening youtube")
                webbrowser.open(f"https://www.youtube.com/")

            # Search YouTube
            elif "search on youtube for" in command:
                query = command.replace("search on youtube for", "")
                speak(f"Searching for {query} on Youtube.")
                print(f"Searching for {query} on Youtube.")
                search_url = "https://www.youtube.com/results?search_query=" + query
                webbrowser.open(search_url)

            # Open Bard
            elif "open google ai" in command or "open bard" in command:
                speak("Opening Bard")
                print("Opening Bard")
                webbrowser.open(f"https://bard.google.com/chat")

            # Open ChatGpt
            elif "open chat gpt" in command:
                speak("Opening ChatGpt")
                print("Opening ChatGpt")
                webbrowser.open(f"https://chat.openai.com/")

            # Open Apps
            elif "go dark" in command:
                text = command.replace("open", "")
                speak(f"Opening {text}")
                print(f"Opening {text}")
                run = f"C:\\Users\\vjjos\\tomato\\apps\\{text}.exe"
                subprocess.run(run)

            # Dev Info
            elif "who made you" in command or "who is your owner" in command or "who is your developer" in command or "who is your dev" in command:
                speak("sir PragneshKumar Singh also known as Maximus")
                print("sir PragneshKumar Singh a.k.a Maximus")




            # Analyze sentiment of a topic
            elif "what do people think about" in command:
                topic = command.replace("what do people think about", "")
                speak("Let me check the sentiment of the topic.")
                print("Let me check the sentiment of the topic.")
                topic = topic
                sia = SentimentIntensityAnalyzer()
                results = openai.Completion.create(
                    engine="davinci",
                    prompt=f"Get opinions about {topic}.",
                    max_tokens=100,
                )
                opinions = results.choices[0].text
                sentiment_score = sia.polarity_scores(opinions)
                if sentiment_score['compound'] >= 0.05:
                    speak(f"Overall, people seem to have a positive sentiment about {topic}.")
                    print("Let me check the sentiment of the topic.")
                elif sentiment_score['compound'] <= -0.05:
                    speak(f"Overall, people seem to have a negative sentiment about {topic}.")
                    print(f"Overall, people seem to have a negative sentiment about {topic}.")
                else:
                    speak(f"Overall, people seem to have a neutral sentiment about {topic}.")
                    print(f"Overall, people seem to have a neutral sentiment about {topic}.")

            # Catch-all response for unrecognized commands
            else:
                print("Here is what i found on internet...")
                question = command
                search_results = google_search(question)
                speak(search_results)
                print(search_results)



        except sr.UnknownValueError:
            print("Sorry, But can you please repeat?")


def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[0].get_text()
    return search_results


def open_browser_in_background(url):
    t = threading.Thread(target=webbrowser.open, args=(url,))
    t.daemon = True
    t.start()


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()


def listen():
    global text
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        cmd = recognizer.recognize_google(audio).lower()
        text = cmd

    except sr.UnknownValueError:
        print("Sorry, But can you please repeat?")

    return text


def google(link):
    webbrowser.open(f"https://www.google.com/search?q={link}")
    cypher()


def scan(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        logging.error(f"Directory '{path}' not found or is not a directory.")
        return

    try:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                os.system(f"clamscan {file_path}")
    except Exception as e:
        logging.error(f"Error executing 'clamscan' on '{file_path}': {str(e)}")


def pro():
    genai.configure(api_key="AIzaSyA9yndda2EQh122n1TR4vr2K1fA8WPkbFc")
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    def gemini():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Pro Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Convert speech to text
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            response = chat.send_message(command, stream=True)
            speak(response.text)
            print(response.text)
            gemini()

        except sr.UnknownValueError:
            print("Sorry, But can you please repeat?")
            gemini()


if __name__ == '__main__':
    cypher()
