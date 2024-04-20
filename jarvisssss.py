import pyttsx3
import speech_recognition as sr
import datetime
import mysql.connector
import wikipedia
import webbrowser
import os
import random
import smtplib
import pywhatkit as kit

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take command from user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

# Function to greet the user
def greet_user():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am JARVIS, how may I assist you?")

# Function to search on wikipedia
def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak(results)
#opening youtube
def open_youtube(url):
    url = 'https://www.youtube.com/'
    webbrowser.open(url)

#opening google
def open_google(url):
    url = 'https://www.google.com/search?q='
    webbrowser.open(url)

# Function to send an email
def send_email(to, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.eusser = 'nirajdas6664521@gmail.com'
    server.password = '666452hateu'
    msg = 'Subject: {}\n\n{}'.format(subject, message)
    server.sendmail('nirajdas6664521@gmail.com', to, msg)
    server.quit()

# Function to play a song on youtube
def play_song(song):
    kit.playonyt(song)

# Function to interact with MySQL database
def interact_with_db():
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="@123Niraj", database="chatbot")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (id INT AUTO_INCREMENT PRIMARY KEY, message TEXT, time TEXT)''')

    # Insert reminder
    def insert_reminder(message, time):
        cursor.execute("INSERT INTO reminders (message, time) VALUES (%s, %s)", (message, time))
        conn.commit()

    # Get reminders
    def get_reminders():
        cursor.execute("SELECT * FROM reminders")
        return cursor.fetchall()

    # Delete reminder
    def delete_reminder(id):
        cursor.execute("DELETE FROM reminders WHERE id=%s", (id,))
        conn.commit()

    return insert_reminder, get_reminders, delete_reminder

# Main function
def main():
    greet_user()
    insert_reminder, get_reminders, delete_reminder = interact_with_db()
    while True:
        query = take_command().lower()

        # Search on wikipedia
        if 'wikipedia' in query:
            query = query.replace('wikipedia', '')
            search_wikipedia(query)

        #search on google
        elif 'google' in query:
            query = query.replace('google', '')
            open_google(url='https://www.google.com/search?q=')

        # Send an email
        elif 'send email' in query:
            speak("To whom should I send the email?")
            to = take_command().lower()
            speak("What should be the subject of the email?")
            subject = take_command().lower()
            speak("What should be the message of the email?")
            message = take_command().lower()
            send_email(to, subject, message)

        # Play a song on youtube
        elif 'play' in query:
            query = query.replace('play', '')
            play_song(query)

        #opening youtube stream
        elif 'open youtube' in query:
            query = query.replace('open youtube', '')
            open_youtube(url="https://www.youtube.com/")

        # Exit the chatbot
        elif 'shutdown' in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()