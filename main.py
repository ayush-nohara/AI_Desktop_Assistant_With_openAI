import os

import speech_recognition as sr
import webbrowser
import datetime
import random
import openai
from config import apikey
from openai import OpenAI

import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")
client = OpenAI(
    api_key=apikey,
)

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Ayan: {query}\n Jarvis:"

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": chatStr,
            }
        ],
        model="gpt-3.5-turbo",

    )
    # todo: Wrap this inside of a try catch block
    # print(respnse["choice"][0]["text"])
    # text += response.choices[0]["text"]
    speaker.Speak(response.choices[0].message.content)

    chatStr += f"{response.choices[0].message.content}\n"
    # text += response.choices[0].message.content
    return chatStr



def ai(prompt):
    openai.api_key = apikey
    text = f"openAI response for prompt: {prompt} \n ************************\n\n"

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "write a meaningful relationship conversation between two people?",
            }
        ],
        model="gpt-3.5-turbo",

    )

    # todo: Wrap this inside of a try catch block
    # print(respnse["choice"][0]["text"])
    # text += response.choices[0]["text"]
    text += response.choices[0].message.content
    if not os.path.exists("openai"):
        os.mkdir("openai")

    with open(f"openai/prompt- {random.randint(1, 234434356)}", "w") as f:
        f.write(text)


def say(text):
    speaker.Speak("Hello I am Chery Lady")
    # os.system(f"say {text}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Chery Lady"


if __name__ == "__main__":
    print("pycharm")
    speaker.Speak("hello, i am your Assistant")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.googlecom"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = "kaho.mp3"
            os.system(f"start {musicPath}")
        if "the time" in query:
            musicPath = "kaho.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speaker.Speak(f"Sir the time is {hour} bajjKke {min} minutes ")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        else:
            ans= chat(query)
            if not os.path.exists("openai"):
                os.mkdir("openai")

            with open(f"openai/prompt- {random.randint(1, 234434356)}", "w") as f:
                f.write(ans)

        # speaker.Speak(query)
