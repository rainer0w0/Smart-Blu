import twitch
import mySQLIntegration
import webbrowser    # Remove when done testing :)
import os
from datetime import datetime
import speech_recognition as sr
import twitchIntegration
import liquipediaIntegration

prefphrases = ["door", "B", "T", "side", "twitch", "open", "CT", "site", "dust","mirage","aztec","overpass","vertigo"]
#Google Cloud Credentials
with open ('############', 'r') as file:
    credential = file.read ()
#Initialize microphone listeners
wakerecognizer = sr.Recognizer()
inputrecognizer = sr.Recognizer()
with sr.Microphone() as source:
    wakerecognizer.adjust_for_ambient_noise(source)
    inputrecognizer.adjust_for_ambient_noise(source)



def wake(): # Checks if "blue" was said (The wake word.) returns False if it was not said, returns True if it was said.
    try: 
        with sr.Microphone() as source:
            print("Currently Listening")
            wake_data = wakerecognizer.listen(source)
            print("Listen Stopped")
            wake = wakerecognizer.recognize_google_cloud (wake_data, language = "en-us", credentials_json = credential, preferred_phrases=prefphrases)
            if "blue" in wake:
                return True
    except sr.UnknownValueError:
        return False
    except sr.RequestError:
        return False



def parseMicrophone(map, side): # Parses the microphone and determines what command is being asked of it. this gonna be BIG EDITTED!!!
    try:
        with sr.Microphone() as source:
            input_data = inputrecognizer.listen(source)
            text = inputrecognizer.recognize_google_cloud (input_data, language = "en-us", credentials_json = credential, preferred_phrases=prefphrases).lower()
        if "how do" in text: # Command for Grenade Lineups
            url = mySQLIntegration.getNadeURL(text, side, map)
            if "http" in url:
                webbrowser.open(url)
                open = True
                while open:
                    with sr.Microphone() as source:
                        input_data = inputrecognizer.listen(source)
                        text = inputrecognizer.recognize_google_cloud (input_data, language = "en-us", credentials_json = credential, preferred_phrases=prefphrases).lower()
                        if "close" in text:
                            os.system("taskkill /im chrome.exe /f")
                            return "Video closed."
            else:
                return "I don't know that grenade!"
        if "transfers" in text: # Shows notifications returned from liquipedia.
            return mySQLIntegration.transNotifications()

        if "on twitch" in text: # opens a stream on twitch
            text = text.split(" ")
            webbrowser.get().open(f"https://player.twitch.tv/?channel={twitchIntegration.searchstream(text[1])}&enableExtensions=true&muted=false&parent=twitch.tv&player=popout&volume=0.1599999964237213")
            open = True
            while open:
                with sr.Microphone() as source:
                    input_data = inputrecognizer.listen(source)
                    text = inputrecognizer.recognize_google_cloud (input_data, language = "en-us", credentials_json = credential, preferred_phrases=prefphrases).lower()
                    if "close" in text:
                        os.system("taskkill /im chrome.exe /f")
                        return "Stream closed."
        print(text)
        if "nade" in text:  
            return mySQLIntegration.availableNades(side,map)

        if "add my" in text:
            return mySQLIntegration.storeNades()

        if "set map" in text:
            text = text.replace("set map ", "")
            map = text
            return "Map changed to " + map

        if "set side" in text:
            text = text.replace ("set side ", "")
            side = text
            return "Side changed to " + side

        if "nevermind" in text:
            return "Okay! Now going to sleep."

        if "close" in text:
            os.system("taskkill /im chrome.exe /f")
            return "Video closed."

        if "play today" in text:
            fixedtext = text.replace("does ", "")
            fixedtext = fixedtext.replace("do ", "")
            fixedtext = fixedtext.replace(" play today ", "")
            return liquipediaIntegration.checkifGame(fixedtext)
         
        if "time" in text:
            return str(datetime.now().strftime('%H:%M'))

        return "Invalid Command!"
    except sr.UnknownValueError:
        return "Invalid Command!"
    except sr.RequestError:
        return "error"



def streamnotifs(streamer): #uses the livenotifs command to return if a streamer is online, and also will ask if you want to open their stream. Opens it if you say an affirmative.
    streamer = streamer
    affirmatives = ['yes','sure','okay','yeah']
    view = True
    while view:
        try:
            with sr.Microphone() as source:
                input_data = inputrecognizer.listen(source)
                text = inputrecognizer.recognize_google_cloud (input_data, language = "en-us", credentials_json = credential, preferred_phrases=prefphrases).lower()
                if any(x in text for x in affirmatives):
                   webbrowser.open("twitch.tv/" + streamer)
                   view = False
                else:
                    if 'no' in text:
                        view = False
        except sr.UnknownValueError:
            None
        except sr.RequestError:
            None