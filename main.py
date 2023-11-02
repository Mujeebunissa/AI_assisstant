# Importing necessary libraries
# selecting voices
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
# text to speech
def say(text):
    engine.say(text)  # Uses pyttsx3 to say the provided text
    # print(text)  # Prints the text to the console
    engine.runAndWait()  # Ensures the speech is spoken and waits for it to finish
    engine.setProperty("rate", 150)  # Sets the speech rate to 150 words per minute


# conversation with AI
import openai
from config import apikey
chatStr = ''  # to store conversation history
def chat(query):
    global chatStr
    # print(chatStr)
    try:
        openai.api_key = apikey
        chatStr += f'user : {query}\nAI : '  # Append user query to chat history
        response = openai.Completion.create(
            model="text-davinci-003",  # davanci alternatives
            prompt=chatStr,
            temperature=0.7,  # hyper parameter
            max_tokens=256,  # prompt tokens limit value
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f"Assistant: {response['choices'][0]['text']}")
        say(response['choices'][0]['text'])
        chatStr += f'{response["choices"][0]["text"]}\n'
        return response['choices'][0]['text']
    except Exception as e:
        print(f'An error occurred: {e}')


# for AI response generation (without conversation history)
import os
def ai_generate(self,prompt):
        try:
            openai.api_key = apikey
            text = f'OpenAI response for prompt: {prompt}\n *****************\n\n'

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,  # hyper parameter
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response['choices'][0]['text'])
            text += response['choices'][0]['text']
            if not os.path.exists('Openai'):
                os.mkdir('Openai')
            with open(f'Openai/{"".join(prompt.split("ai")[1:])}.txt', 'w') as f:
                f.write(text)  # Save AI response to a text file

        except Exception as e:
            print(f'An error occurred: {e}')



# To tell weather
import requests
from bs4 import BeautifulSoup
def get_weather(query):
    try:
        # Check if the query contains "temperature" or "weather"
        # prompt engineering
        keyword = 'temperature' if 'temperature' in query else 'weather'

        words = query.split()
        indexes = words.index(keyword) + 1  # finding the index of keyword
        place = ' '.join(words[indexes:])  # Extract the location information from the query
        url = f'https://www.google.com/search?q={place} {keyword}'  # Construct a Google search URL
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.find('div', {'class': 'BNeawe'}).text
        weather = f'Current {keyword} {place} is {info}'
        print(f'Assistant: {weather}')
        return weather
    except Exception as e:
        return f'An error occurred: {e}'


# To get news headlines
from config import gnews_apikey
import json
import urllib.request
def get_news():
    print(f'Assistant: What type of news are you interested in?, is it general, world, nation, business, technology, entertainment, sports, science or health')
    say("What type of news are you interested in?, is it general, world, nation, business, technology, entertainment, sports, science or health ?")
    category = ''
    categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science',
                  'health']
    user = takeCommand()
    for i in user.split():
        if i in categories:
            category += i
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=in&max=10&apikey={gnews_apikey}"
    print(f'Assistant: Here are the top headlines on {category}')
    say(f'Here are the top headlines on {category}')
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        for i in range(3):
            # articles[i].title
            print(f"Title: {articles[i]['title']}")
            say(f"{articles[i]['title']}")
            # articles[i].description
            print(f"Description: {articles[i]['description']}")
            say(f"{articles[i]['description']}")


# To open any website
import webbrowser
from googlesearch import search
def open_website(query):
    try:
        search_results = list(search(query, num_results=1))
        if search_results:
            website_url = search_results[0]
            # Extract the site name from the URL
            site_name = website_url.split('www.')[-1].split('.')[0]
            print(f'Assistant: Opening {site_name} ...')
            say(f"Opening {site_name} ...")
            webbrowser.open(website_url)
        else:
            print("Assistant: Sorry, I couldn't find any relevant websites")
            say("Sorry, I couldn't find any relevant websites.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# To show best route from 1 des to other
def maps(des1, des2):
    url = "https://www.google.com/maps/dir/" + des1 + "/" + des2
    webbrowser.open(url)


# To Play a video on YouTube
import pywhatkit
def play_youtube_videos(query):
    video = query.replace('play'.lower(), '').replace('Jarvis'.lower(), '')
    # response engineering here
    print(f'Assistant: playing {video}, enjoy.')
    say(f'playing {video}, enjoy.')
    pywhatkit.playonyt(video)


import pywhatkit as kit
import datetime
def whatsapp_message(query):
    print(f'Assistant: To whom you want to message?, please enter a phone number below: ')
    say('To whom you want to message?, please enter a phone number below: ')
    number = int(input('Phone Number: '))
    print(f'Assistant: for confirmation, please enter phone number again')
    say('for confirmation, please enter phone number again')
    confirm_number = int(input('Confirm Phone Number: '))
    if confirm_number == number:
        phone_number = f'+91{confirm_number}'
        print(f'Assistant: what message do you want to send')
        say('what message do you want to send')
        message = takeCommand()
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 1  # Send the message one minute from now
        print(f"Scheduled to send at: {hour}:{minute}")
        print(f'Assistant: Your message is being sent,  please wait')
        say("Your message is being sent,  please wait")
        kit.sendwhatmsg(phone_number, message, hour, minute)
        print(f'Assistant: Message sent successfully!')
        say('Message sent successfully!')
    else:
        print('Assistant: Sorry, the phone number you entered is incorrect.')
        say('Sorry, the phone number you entered is incorrect.')
        print('Assistant: Please try again.')
        say('Please try again.')
        whatsapp_message(query)


# automate email
import smtplib
from email.message import EmailMessage
def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('syedatasneem958@gmail.com', 'ozrh jbfx qqvl byku')
    email = EmailMessage()
    email['From'] = 'Sender_Email'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)
def get_email_info():
    print('Assistant: To Whom you want to send email, please enter a email address below ')
    say('To Whom you want to send email, please enter a email address below ')
    receiver = input("Enter The Receiver's Email:")
    receiver = receiver
    print('Assistant: for confirmation, please enter email address again')
    say('for confirmation, please enter email address again')
    confirm_receiver = input("Confirm Email Address: ")
    # print(receiver)
    if confirm_receiver==receiver:
        print('Assistant: What is the subject of your email?')
        say('What is the subject of your email?')
        subject = takeCommand()
        print('Assistant: Tell me the message of your email')
        say('Tell me the message of your email')
        message = takeCommand()
        send_email(receiver, subject, message)
        print('Assistant: Your email is sent')
        say('Your email is sent')
        print('Assistant: Do you want to send more email?')
        say('Do you want to send more email?')
        send_more = takeCommand()
        if 'yes' in send_more:
            get_email_info()
        else:
            print('Assistant: Sure, just give me a shout if youd like to send more emails')
            say('Sure, just give me a shout if youd like to send more emails')
    else:
        print('Assistant: Sorry, the email address you entered is incorrect. Please try again')
        say('Sorry, the email address you entered is incorrect. Please try again')
        print('Assistant: Please try again.')
        say('Please try again.')
        get_email_info()


# generates a random response phrase for a jarvis
import random
# Counter just for interacting purposes
interaction_counter = 0
def activate_assistant():
    starting_chat_phrases = ["Yes , how may I assist you?",
                             "Yes, What can I do for you?",
                             "How can I help you, ?",
                             "Jarvis at your service, what do you need?",
                             "Jarvis here, how can I help you today?",
                             "Yes, what can I do for you today?",
                             "Yes , what's on your mind?",
                             "Jarvis ready to assist, what can I do for you?",
                             "At your command,. How may I help you today?",
                             "Yes, . How may I be of assistance to you right now?",
                             "Yes , I'm here to help. What do you need from me?",
                             "Yes, I'm listening. What can I do for you, ?",
                             "How can I assist you today,?",
                             "Jarvis here, ready and eager to help. What can I do for you?",
                             "Yes, . How can I make your day easier?",
                             "Yes , what's the plan? How can I assist you today?",
                             "Yes, I'm here and ready to assist. What's on your mind,?"]

    continued_chat_phrases = ["yes", "I'm all ears", "go ahead, I'm listening", " I'm all set to listen up", "I'm fully engaged, share your thoughts", " I'm all set to hear you out"]

    random_chat = ""
    if (interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else:
        random_chat = random.choice(continued_chat_phrases)

    return random_chat


# front-end work
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_JarvisUi

import speech_recognition as sr

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.task_execution()

    # take command from user
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            # r.energy_threshold = 600
            audio = r.listen(source)
            try:
                print('recognizing')
                query = r.recognize_google(audio, language='en-us')  # Convert audio to text  # US accent parameter
                print(f'You: {query}')
                query = query.lower()  # Convert text to lowercase
                return query
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand your speech.")
            except sr.RequestError as e:
                print(f"Sorry, an error occurred: {e}")

    # To perform tasks
    def perform_task(self):
        while True:
            self.query = self.takeCommand()  # Capture user's voice query
            # chat(query)
            if self.query is not None:
                try:
                    if 'using ai'.lower() in self.query:
                        ai_generate(prompt=self.query)
                        print('Assistant: Done. is there anything else I can help you with?')
                        say('done. is there anything else I can help you with?')
                        # Generate AI response based on the user's query

                    elif 'open camera'.lower() in self.query:
                        print('Assistant: opening camera')
                        say('opening camera')
                        os.system('start microsoft.windows.camera:')

                    elif 'open notepad'.lower() in self.query:
                        print('Assistant: opening notepad')
                        say('opening notepad')
                        os.system('start notepad')

                    elif 'open command prompt'.lower() in self.query:
                        print('Assistant: opening command prompt')
                        say('opening command prompt')
                        os.system('start cmd')

                    elif 'open calculator'.lower() in self.query:
                        print('Assistant: opening calculator')
                        say('opening calculator')
                        os.system('start calc')

                    elif 'open file explorer'.lower() in self.query:
                        print('Assistant: opening file explorer')
                        say('opening file explorer')
                        os.system('start explorer')

                    elif 'temperature'.lower() in self.query or 'weather'.lower() in self.query:
                        say(get_weather(self.query))
                        # calling the function

                    elif 'updated news'.lower() in self.query:
                        say(get_news())
                        # calling the function

                    # Feature source list  (websites)
                    elif "open".lower() in self.query:
                        query_parts = self.query.split()
                        website_query = " ".join(query_parts[query_parts.index("open") + 1:])
                        # Perform the web search and open the top result
                        open_website(website_query)

                    elif 'route'.lower() in self.query:
                        route = self.query.split('from')[-1].split('to')
                        print(f'Assistant: The best route from {route[0]} to {route[1]} is:')
                        say(f'The best route from {route[0]} to {route[1]} is:')
                        maps(route[0], route[1])

                    elif 'play'.lower() in self.query:
                        say(play_youtube_videos(self.query))
                        # import os
                        # .startfile(musicPath2)

                    elif 'the time'.lower() in self.query:
                        strfTime = datetime.datetime.now().strftime('%I:%M%p')
                        strfTime = strfTime.lstrip('0').replace(':', ' : ')
                        # response engineering here
                        print(f'Assistant: The Time is {strfTime}')
                        say(f'The Time is {strfTime}')  # Tell the current time

                    # reset command here
                    elif 'reset chat'.lower() in self.query:
                        global chatStr
                        chatStr = ''  # Reset the chat history
                        print('Assistant: Chat is reset')
                        say('Chat is reset')

                    # elif 'sleep'.lower() in query or 'you can sleep'.lower() in query or 'sleep now'.lower() in query:
                    #     say("okay. I'm going to sleep. You can wake me up anytime you need assistance.")
                    #     break

                    elif 'whatsapp message'.lower() in self.query:
                        whatsapp_message(self.query)
                        # calling the function

                    elif "today's date".lower() in self.query or "date today".lower() in self.query:
                        # response engineering here
                        print(f'Assistant: the date is {datetime.date.today()}')
                        say(f'the date is {datetime.date.today()}')  # Tell the current date

                    elif "send email".lower() in self.query or "send an email".lower() in self.query:
                        get_email_info()
                        # calling the function

                    elif 'exit'.lower() in self.query.lower():
                        print(
                            'Assistant: Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!')
                        say('Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!')
                        exit()

                    elif 'jarvis'.lower() in self.query:
                        chat(self.query)

                    else:
                        break

                except Exception as e:
                    print(e)

    def task_execution(self):
        if __name__ == '__main__':
            while True:
                print("say 'Jarvis' to start")
                self.query = self.takeCommand()
                if self.query is not None:
                    if 'jarvis'.lower() in self.query:
                        global interaction_counter
                        interaction_counter += 1
                        phrases = activate_assistant()
                        print(f'Assistant: {phrases}')
                        say(phrases)
                        self.perform_task()

                    if 'exit'.lower() in self.query:
                        print(
                            'Assistant: Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!')
                        say('Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!')
                        exit()


import os
import webbrowser as web
import sys

startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton_start.clicked.connect(self.startTask)
        self.ui.pushButton_exit.clicked.connect(self.close)
        self.ui.pushButton_chrome.clicked.connect(self.chrome_app)
        self.ui.pushButton_whatsapp.clicked.connect(self.whatsapp_app)
        self.ui.pushButton_youtube.clicked.connect(self.yt_app)

    def chrome_app(self):
        os.startfile("C://Program Files//Google//Chrome//Application//chrome.exe")
    def yt_app(self):
        web.open('https://www.youtube.com/')
    def whatsapp_app(self):
        web.open('https://web.whatsapp.com/')
    def startTask(self):

        self.ui.movie = QtGui.QMovie("C://Users//MUEEBUNISSA//OneDrive//Desktop//jarvis AI\Black.png")
        self.ui.bg_1.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C://Users//MUEEBUNISSA//OneDrive//Desktop//jarvis AI//spheres1_ai_improvisation_by_gleb.gif")
        self.ui.GIF_1.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C://Users//MUEEBUNISSA//OneDrive//Desktop//jarvis AI//1d735ad8eee8350adc96d50e1421ee6d.gif")
        self.ui.GIF_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C://Users//MUEEBUNISSA//OneDrive//Desktop//jarvis AI//coollogo_com-81931662.gif")
        self.ui.GIF_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()


    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss ap')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.date.setText(label_date)
        self.ui.time.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


# open zomato and show me pista house offers in hyderabad
# Jarvis, open flipkart and show me the iPhone 15 Pro Max

