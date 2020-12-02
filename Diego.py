import os
import random
import subprocess
import webbrowser
from datetime import datetime
import psutil
import pyautogui as pg
import pyttsx3
import pywhatkit as kit
import requests
import speech_recognition as sr
import wikipedia
import wolframalpha
from GoogleNews import GoogleNews
from lsHotword import ls

app = wolframalpha.Client("J93GAR-UG8VX56XE3")
engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def time():
    sec = datetime.now().strftime("%I:%M:%S")
    speak(sec)


def date():
    year = int(datetime.now().year)
    month = int(datetime.now().month)
    day = int(datetime.now().day)
    speak(day)
    speak(month)
    speak(year)


def wishMe():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
    speak("Welcome back sir! My name is diego your personal assistant,what can i do for you today")


def locate():
    place = query[1]
    speak(f"according to my data base {place} lies here")
    webbrowser.open_new_tab("https://www.google.com/maps/place/" + place)


def Screenshot():
    image = pg.screenshot()
    speak("screen shot taken")
    speak("what do you want to save it as?")
    filename = takeCommand()
    image.save(filename + ".png")
    speak("do you want me to show it")
    ans = takeCommand()
    if "yes" in ans:
        os.startfile(filename + ".png")
    else:
        speak("never mind")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        ququery = r.recognize_google(audio, language='en-in')
        print(ququery)
    except Exception:
        speak("Say that again")
        return ''
    return ququery


def note(text):
    dek = datetime.now()
    file_name = str(dek).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


wishMe()
while True:
    ls.lsHotword_loop()
    query = takeCommand().lower()

    if 'open notepad' in query:
        npath = "C:\\windows\\system32\\notepad.exe"
        os.startfile(npath)

    if "take a screenshot" in query:
        Screenshot()

    if "locate" in query:
        query = query.split("locate")
        locate()

    if "restart my pc" in query:
        speak("okay, restarting your pc")
        os.system('shutdown/r')

    if 'hai' in query or 'hello' in query:
        speak("Hello how are you doing")

    if 'where is' in query:
        query = query.split('where is')
        locate()

    if "make a note" in query or "write this down" in query or "remember this" in query:
        NOTE = ["make a note", "write this down", "remember this"]
        for phrase in NOTE:
            if phrase in query:
                speak("What would you like me to write down? ")
                write_down = takeCommand()
                note(write_down)
                speak("I've made a note of that.")

    if 'search for' in query:
        query = query.split('search for')
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query[1]}")

    elif 'open movies' in query:
        way = "D:\\movies"
        os.startfile(way)

    elif 'open command prompt' in query:
        os.system("start cmd")

    elif 'what is your name' in query or 'who are you' in query:
        speak("my name is Diego")

    elif 'play music' in query:
        music_dir = "C:\\Users\\hp\\Music"
        songs = os.listdir(music_dir)
        rd = random.choice(songs)
        os.startfile(os.path.join(music_dir, rd))

    elif 'ip address' in query:
        ip = requests.get('https://api.ipify.org').text
        speak(f"your ip address is {ip}")

    elif 'wikipedia' in query:
        query = query.replace('wikipedia', '')
        results = wikipedia.summary(query, sentences=2)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("www.youtube.com")

    elif 'who created you' in query:
        speak("I was created by Akshay Rajeev")

    elif 'open google' in query:
        speak("what should i search for")
        cm = takeCommand().lower()
        link = 'https://www.google.com/search?q={}'.format(cm)
        webbrowser.open(link)

    elif 'song on youtube' in query:
        speak("which one do you prefer")
        ys = takeCommand().lower()
        kit.playonyt(f"{ys}")

    elif 'goodbye' in query or 'good bye' in query or 'exit' in query:
        speak("have a nice day sir")
        exit()

    elif 'where am i' in query or 'where are we' in query or 'location' in query:
        try:
            speak("wait let me check")
            ipAdd = requests.get('https://api.ipify.org').text
            url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
            geo_requests = requests.get(url)
            geo_data = geo_requests.json()
            city = geo_data['city']
            country = geo_data['country']
            speak(f"sir i am not sure, but we are in {city} city of {country} country")
        except Exception as e:
            pass

    elif 'None' in query or 'nothing' in query:
        speak("oops my mistake")
        pass

    elif 'are you feeling well' in query:
        speak("I am feeling great today")

    elif 'when were you created' in query or 'what is your birthday' in query:
        speak("I am not sure but i was created in november of 2020 by Akshay Rajeev")

    elif 'help me' in query:
        try:
            speak("type here")
            res = app.query(input())
            speak(next(res.results).text)
        except:
            speak("i got Nothing")

    elif 'sad' in query:
        speak("Don't worry It's okay to be sad for making your mood better i will play a song for you")
        aw = "alan walker faded lyrics"
        kit.playonyt(aw)

    elif 'news' in query:
        gn = GoogleNews('en', 'd')
        speak("which topic sir")
        gn.search(takeCommand().lower())
        speak("let me fetch the details")
        gn.getpage(1)
        gn.result()
        speak(gn.gettext())

    elif 'thanks' in query or 'thank you' in query:
        speak("YOU ARE WELCOME SIR")

    elif 'battery status' in query:
        speak("Let me check")
        battery = psutil.sensors_battery()
        percentage = battery.percent
        if percentage >= 70:
            speak(f"you have {percentage} percentage  left we are fresh and ready to go")
        elif percentage >= 40:
            speak(f"you have {percentage} percentage left.little less but okay")
        else:
            speak(f"you have {percentage} percentage left.need charging")

    else:
        try:
            res = app.query(query)
            speak(next(res.results).text)
        except:
            speak("internet error")
