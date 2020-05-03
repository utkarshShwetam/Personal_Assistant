import pyttsx3
import datetime
import speech_recognition as recog
import wikipedia
import webbrowser
import os
import sys
import winreg
import shlex
import spotipy
import random
import pyowm
import requests
import json 
import bs4
import tkinter as t
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import config as con


#Microsoft Speech Api sapi5 used
engine=pyttsx3.init()
voices=engine.getProperty('voices')
#print(voices[-1].id)
engine.setProperty('voice',voices[-1].id)
#print("Hello world")

def open_sir_command():
    speak("Opening for you sir")
#Finds the directory of google chrome
def try_find_chrome_path():
    result = None
    if winreg:
        for subkey in ['ChromeHTML\\shell\\open\\command', 'Applications\\chrome.exe\\shell\\open\\command']:
            try: result = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, subkey)
            except WindowsError: pass
            if result is not None:
                result_split = shlex.split(result, False, True)
                result = result_split[0] if result_split else None
                if os.path.isfile(result):
                    break
                result = None
    else:
        expected = "google-chrome" + (".exe" if os.name == 'nt' else "")
        for parent in os.environ.get('PATH', '').split(os.pathsep):
            path = os.path.join(parent, expected)
            if os.path.isfile(path):
                result = path
                break
    return result
#Jarvis speaking capability
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#Uses open_Weather_Map Api that is pyowm to get temperature
def temparature_call():
    list1=[]
    res=requests.get(con.WEB_LINK)
    data=res.json()
    city=data['city']
    country_code=data['country'].lower()
    owm = pyowm.OWM(con.API_KEY)
    observation = owm.weather_at_place(city+','+country_code)
    w = observation.get_weather()
    temperature = w.get_temperature('celsius')
    for key in temperature.keys():
        list1.append(temperature[key])
    speak(f'The current temparature at your location is {list1[0]} deggree celsius')    
#Uses open_Weather_Map Api that is pyowm to get weather status
def weather_api_use():
    list=[]
    res=requests.get(con.WEB_LINK)
    data=res.json()
    city=data['city']
    country_code=data['country'].lower()
    owm = pyowm.OWM(con.API_KEY)
    observation = owm.weather_at_place(city+','+country_code)
    w = observation.get_weather()
    wind = w.get_wind()
    temperature = w.get_temperature('celsius')
    status=w.get_status()
    speak(f'The weather in your location is {status}')
    #tomorrow = pyowm.timeutils.tomorrow()
    #print(type(wind))
    for key in temperature.keys():
        list.append(temperature[key])
    speak(f'The current temparature at your location is {list[0]} deggree celsius with a minimum of {list[2]} deggree celsius')
    for key in wind.keys():
        list.append(wind[key])
    speak(f'Speed of winnnddd is{list[4]}  at a degggree of {list[5]}')
    humid_val=w.get_humidity()
    speak(f'with a humidity of {humid_val}')
    #print(tomorrow)
#Wishes me according to time
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning Sir")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")

    speak("I am Laaajjo! Your personal assistant")
    speak("How may i help you sir?")
#Uses ipinfo.io API and website to get your location and provide it to the weather Api function
def ipinfoio_api_use():
    res=requests.get(con.WEB_LINK)
    data=res.json()
    city=data['city']
    region=data['region']
    location=data['loc'].split(',')
    latitude=location[0]
    longitude=location[1]
    zone=data['timezone']
    speak(f'You current city is {city} located in {region} situated at latitude of {latitude} and longitude of {longitude} in the zone {zone}')
#To take microphone input and convert to string array
def takeCommand():
    rnize=recog.Recognizer()
    with recog.Microphone() as source:
        speak("I am listening")
        rnize.pause_threshold=1
        audio=rnize.listen(source)
    
    try:
        speak("Recognizing your command")
        query = rnize.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(f'Network Error {e}')
        speak("Say that again please...")
        return "None"
    return query
#To get top stories from google news feed using Bs4 library
def news_get():
    news_url=con.NEWS_URL
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()

    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    # Print news title, url and publish date
    for news in news_list:                             
      speak(news.title.text)
      #print(news.link.text)
      #print(news.pubDate.text)
      #print("-"*60)
#To stop using button
def stop_ai():
    exit()
def main():
    speak("Hello")
    wishme()
    querysaid=takeCommand().lower()
    var=try_find_chrome_path()
    #your google chrome browser location 
    webloc=con.WEBLOC
    #print(var)
    #Logic for executing commmands
    if (querysaid=='none'):
        speak("You didnt said anything sir")

    if 'hey jarvis' in querysaid:
        speak('Yeah! Thats me sir.')
        speak('Please tell me how may i help you sir?')
        querysaid=takeCommand().lower()

    if 'how are you' in querysaid:
        speak("I am doing great sir ! how may i help you?")
        querysaid=takeCommand().lower()

    if 'wikipedia' in querysaid:
        speak("Searching Wikipedia Sir")
        querysaid=querysaid.replace("wikipedia","")
        results=wikipedia.summary(querysaid,sentences=2)
        speak("As per Wikipedia")
        print(results)
        speak(results)
    elif ('open a website') in querysaid:
        if(var=='none'):
            speak("Please install Google chrome sir to open web pages")
        else:
            speak("Tell the url of website sir like for example google.com to open google")
            website=takeCommand().lower()
            #open_sir_command()
            #print(website)
            if(website=='none'): 
                speak("No website said by you sir")
            else:
                open_sir_command()
                webbrowser.get(webloc).open(website)
    elif 'play music' in querysaid:
        music_dir=con.MUSIC_DIR
        if(len(music_dir) == 0):
            speak("Please provide your music directory")
        else:
            songs=os.listdir(music_dir)
            #print(songs)
            ran_song=random.randint(0,len(songs)-1)
            open_sir_command()
            os.startfile(os.path.join(music_dir,songs[ran_song]))
    elif 'the time' in querysaid:
        str_time=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir,The time is {str_time}")
    elif 'the weather' in querysaid:
        weather_api_use()
    elif 'the temperature' in querysaid:
        temparature_call()
    elif 'my location' in querysaid:
        ipinfoio_api_use()
    elif 'google search' in querysaid:
        speak("Tell me What do you want to search sir")
        search_query=takeCommand().lower()
        url_search=con.URL_SEARCH
        new=2
        open_sir_command()
        webbrowser.get(webloc).open(url_search+search_query,new=new)
        speak("Searching for you sir")
    elif 'latest news' in querysaid:
        news_get()
    elif 'stop' in querysaid:
        exit()
    else:
        speak("I cant perform that for now. Sorry sir!")

if __name__ == "__main__":
    main()



