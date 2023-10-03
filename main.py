import datetime  # Provides functionality to work with dates and times.
import speech_recognition as sr  # Enables speech recognition for capturing voice input.
import os  # Provides operating system-related functions, like file operations.
import win32com.client  # Allows you to use the Windows Speech API for text-to-speech conversion.
import webbrowser  # Provides functions for opening web browsers.
import openai  # Gives access to the OpenAI API for natural language processing.
from config import apikey
import random
import pywhatkit  # Offers various utilities for working with text and web.
import requests  # Allows you to send HTTP requests and handle responses.
from bs4 import BeautifulSoup  # A library for web scraping and parsing HTML.
# import searchnow

# Initialize a global chatStr variable to store conversation history
chatStr = ''


# Defining a function for the AI to respond to user queries
def chat(query):
    global chatStr
    # print(chatStr)
    try:
        openai.api_key = apikey
        chatStr += f'user : {query}\nAI : '  # Append user query to chat history
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        say(response['choices'][0]['text'])
        chatStr += f'{response["choices"][0]["text"]}\n'
        return response['choices'][0]['text']
    except Exception as e:
        print(f'An error occurred: {e}')


# Define a function for AI response generation (without conversation history)
def ai(prompt):
    try:
        openai.api_key = apikey
        text = f'OpenAI response for prompt: {prompt}\n *****************\n\n'

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response['choices'][0]['text'])
        text += response['choices'][0]['text']
        if not os.path.exists('Openai'):
            os.mkdir('Openai')
        # with open(f'Openai/prompt- {random.randint(1,2343434356)}', "w") as f:
        with open(f'Openai/{"".join(prompt.split("intelligence")[1:])}.txt', 'w') as f:
            f.write(text)  # Save AI response to a text file

    except Exception as e:
        print(f'An error occurred: {e}')


# Define a function to speak text using Windows Speech API
def say(s):
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    while 1:
        return speaker.Speak(s)


# Define a function to capture user voice input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        # r.pause_threshold = 1
        # r.energy_threshold = 400
        audio = r.listen(source)
        try:
            print('recognizing')
            query = r.recognize_google(audio, language='en-IN')  # Convert audio to text
            print(f'user said: {query}')
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
        except sr.RequestError as e:
            print(f"Sorry, an error occurred: {e}")


def get_weather(query):
    try:
        # Check if the query contains "temperature" or "weather"
        keyword = 'temperature' if 'temperature' in query else 'weather'

        words = query.split()  # Split the user's query into words
        indexes = words.index(keyword) + 1  # Find the index of the keyword (temperature or weather)
        place = ' '.join(words[indexes:])  # Extract the location information from the query
        url = f'https://www.google.com/search?q={place} {keyword}'  # Construct a Google search URL
        r = requests.get(url)  # Send an HTTP GET request to the Google search URL
        soup = BeautifulSoup(r.text, 'html.parser')  # Parse the HTML content of the search result
        info = soup.find('div', {'class': 'BNeawe'}).text  # Find and extract temperature or weather information
        return f'Current {keyword} in {place} is {info}'  # Return a formatted response
    except Exception as e:
        return f'An error occurred: {e}'  # Handle any errors that may occur


# Main program loop
if __name__ == '__main__':
    say("Hello, Jarvis AI here")
    while True:
        query = takeCommand()  # Capture user's voice query
        sites = [['youtube', 'https://youtube.com'], ['wikipedia', 'https://www.wikipedia.com'],
                 ['google', 'http://www.google.com']]
        for i in sites:
            if f'open {i[0]}'.lower() in query.lower():
                say(f'Opening {i[0]} ...')
                webbrowser.open(i[1])  # Open specified websites

        if 'play'.lower() in query.lower():
            song = query.replace('play'.lower(), '').replace('Jarvis'.lower(), '')
            say(f'playing {song}, enjoy.')
            pywhatkit.playonyt(song)  # Play a song on YouTube
            # os.startfile(musicPath2)

        elif 'the time'.lower() in query.lower():
            strfTime = datetime.datetime.now().strftime('%H:%M: %p')
            say(f'the time is {strfTime}')  # Tell the current time

        elif 'using ai'.lower() in query.lower():
            ai(prompt=query)  # Generate AI response based on the user's query

        elif 'temperature'.lower() in query.lower() or 'weather'.lower() in query.lower():
            say(get_weather(query))
            # say(temperature_info)

        elif 'Quit'.lower() in query.lower():
            say('okay, Goodbye, have a nice day')
            exit()  # Quit the program

        elif 'reset chat'.lower() in query.lower():
            chatStr = ''  # Reset the chat history
            # say(query)

        else:
            print('Chatting....')
            chat(query)  # Chat with the AI



# can talk to Jarvis casually
# can open YouTube videos , play songs
# can tell time
# can reset chat
# can use artificial intelligence to write an essay or code or something like that