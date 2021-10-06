
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import psutil
import pyautogui
import screen_brightness_control as sbc
import ctypes
import keyboard

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[3].id)

def email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('abhisheksinghal862@gmail.com', 'Abhi@8171576670')
    server.sendmail('abhisheksinghal862@gmail.com', to, content)
    server.close


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    pass

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak('Good morning!')

    elif hour>=12 and hour<18:
        speak('Good Afternoon!')

    else:
        speak('Good Evening!')
    
    speak('I am Morgan sir. Please tell me how can I help you')
    

def takeCommand():
    # it take micrphone input from the user and return string output
    r= sr.Recognizer()

    with sr.Microphone() as source:
        print('Listning.........')
        r.pause_threshold = 1
        r.energy_threshold = 2400
        audio = r.listen(source)
    try:
        print('recognising....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print('e')
        print('Say that again please......')
        return "None"
    return query

if __name__=="__main__":
    # speak('Abhishek is good boy')
    wishme()
    while True:
        query = takeCommand().lower()
        # logic executing task based on query
        if 'wikipedia' in query:
            speak('Searching...............')
            query = query.replace('wikipedi', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to wikipedia')
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
            speak('As your wish sir')

        elif 'open hotstar' in query:
            webbrowser.open('https://www.hotstar.com/in')
            speak('Opening hotstar')

        elif 'open go go' in query:
            webbrowser.open('https://gogoanime.vc/strike-blood-episode-18')
            speak('Opening gogo anime')

        elif 'open google' in query:
            webbrowser.open('google.com')
            speak('Done')

        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')
            speak('Ok sir!')
        
        elif 'play music' in query:
            music_dir = 'F:\\gabanana'
            songs = os.listdir(music_dir)
            rs = random.randint(0,len(songs)-1)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[rs]))
            speak('Surprise!')
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')

        elif 'open code' in query:
            codepath = "C:\\Users\\Abhishek Singhal\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)
            speak('Running Visual Studio code')

        elif 'email to abhishek' in query:
            try:
                speak('What should I say')
                content = takeCommand()
                to = 'abhisheksinghal861@gmail.com'
                email(to, content)
                speak('Email has sent')
            except Exception as e:
                speak('Sorry Abhishek sir i unable to sent this mail')
        
        elif 'open pi' in query:
            shellpath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2021.2\\bin\\pycharm64.exe"
            os.startfile(shellpath)
            speak('Running Py Charm ......it may take time')

        elif 'open chrome' in query:
            chromepath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chromepath)
            speak('running google chrome')

        elif 'open hydra' in query:
            chromepath = "F:\\"
            os.startfile(chromepath)
            speak('Distroy it')

        elif 'open friday' in query:
            chromepath = "E:\\"
            os.startfile(chromepath)
            speak('Thats my pleasure')

        elif 'open excel' in query:
            exclepath = "C:\\Program Files\\Microsoft Office\\root\\\Office16\\EXCEL.EXE"
            os.startfile(exclepath)
            speak('work hard')

        elif 'battery percentage' in query:
            try:
                battery = psutil.sensors_battery()
                percent = battery.percent
                speak(f'{percent} persent')
            except Exception as e:
                speak('Cannot able to tell')

        elif 'volume up' in query:
            pyautogui.press('volumeup')
            speak('Done sir!')

        elif 'volume down' in query:
            pyautogui.press('volumedown')
            speak('Done sir!')


        elif 'mute computer' in query:
            speak('Done sir!')
            pyautogui.press('volumemute')

        elif 'speak it' in query:
            speak('I am hearing')
            listening = takeCommand()
            speak(listening)

        elif 'set brightness' in query:
            speak('On my mark sir')
            try:
                brightness = int(takeCommand())
                a = sbc.set_brightness(brightness)
                speak(f'Computer brightness set to {brightness}')
            except Exception as e:
                speak('Sorry sir can not able to do it')

        elif 'hello morgan' in query:
            speak('I am always with you! just give me command')

        elif 'who are you' in query:
            speak('I am virtual asistance of Abhishek and control the input output of this computer, I programmed by Abhishek on 27th september 2021')


        elif 'excellent' in query:
            speak('Thankyou sir')

        elif 'go to hell' in query:
            speak('I try hard next time')
        
        elif 'lock the pc' in query:
           a = ctypes.windll.user32.LockWorkStation()
           speak('as your wish sir')
      
        elif 'shutdown the pc' in query:
            speak('Warning the pc going to shutdown are you ready!')
            a = takeCommand()
            if 'yes' in a:
                b = os.system("shutdown /s /t 1")
            else:
                pass
            
        elif 'restart the pc' in query:
            speak('Warning the pc going to restart are you ready!')
            a = takeCommand()
            if 'yes' in a:
                speak('Going to meet you soon sir')
                a = os.system("shutdown /r /t 1")
            else:
                pass

        elif 'control keyboard' in query:
            speak('Keyboard hacked what you want to type')
            while True:
                a = takeCommand()
                try:
                    if 'exit control' in a:
                        speak('Control of keyboard is over')
                        break
                    else:
                         keyboard.write(a)
                except Exception as e:
                        speak('Sorry i failed for further process')

        elif 'today news' in query:
            import requests , json

            try:
                speak("Today's News")
                url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=7a0c809e57884bfa895bc61a6420b347"
                r = requests.get(url).text
                r_dict = json.loads(r)
                rr = r_dict['articles']
                for count, txt in enumerate(rr):
                    print(f"News {count} is {txt['title']}")
                    speak(f"News {count} is {txt['title']}")

                print("Today's headlines are complete")
                speak("Today's headlines are complete")
            except Exception as e:
                speak('Can not able to diliver news')

