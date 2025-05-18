# pip install speechrecognition pyaudio
# pip install setuptools
# pip install webbrowser - built in function
# pip install pocketsphinx
# import speech_recognition as sr
# print(sr.Microphone.list_microphone_names())

#Imports
import speech_recognition as sr
import webbrowser
import pyttsx3   #Used for text-speech(it is an text-speech package)
import difflib
import favourite_music as musiclibrary
import requests
from openai import OpenAI
from datetime import datetime

recognizer = sr.Recognizer()  
engine = pyttsx3.init()         #We initialise pyttsx3.
newsApi = NEWS_API

#Functions:
def speak(text):
    engine.say(text)
    engine.runAndWait()    #This is used to inform program that please wait after you run, so we can hear the call.

def openAi(command):
    client = OpenAI(
    api_key = API KEY,
)

    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages = [
                {"role":"system" , "content":"you are a virtual assitant named jarvis skilled in general tasks like alexa and google cloud, give me short description"},
                {"role":"user" , "content":command}
        ]
        )

    return completion.choices[0].message.content

def socialMedia(name):
    # if name in c.lower() and "open" in c.lower():
    speak(f"opening {name}...")
    webbrowser.open(f"https://{name}.com")
    return f"Opening {name}"

def processCommand(c):
    #Command should be in format "open instagram":
    if c.lower().startswith("open"):
        name = c.lower().split(" ")[1]
        return socialMedia(name)

    #Music/song play:
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "", 1).strip()  # gets full name like 'play attention song'
        if song.endswith("song"):
            song = song.rsplit("song", 1)[0].strip()
        try:
            speak(f"playing {song}...")
            link = musiclibrary.music[song]
            webbrowser.open(link)
        except Exception as e:
            print(f"❌ Song '{song}' not found in your music library.")
        return f"Playing {song}"

    #News headlines:
    elif "news" in c.lower():
        speak("Reading News...")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsApi}")
        if r.status_code == 200:
            data = r.json() #Parse the json response

            articles = data.get('articles',[])#Extract the articles

            #print headlines
            max_title = 3
            i=0
            for article in articles:
                title = article.get('title', '')
                if title:
                    speak(title)
                    i += 1
                # Pause after every 3 headlines
                if i % max_title == 0:
                    speak("Would you like me to continue?")
                    with sr.Microphone(device_index=2) as source:
                        r = sr.Recognizer()
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio = r.listen(source, timeout=2, phrase_time_limit=4)
                        reply = r.recognize_google(audio, language='en-IN')
                        print(reply)

                    if "no" in reply or "stop" in reply:
                        speak("Okay, stopping now.")
                        break
        return "Reading Updated News"
    
    #Response by AI:
    else:
        output = openAi(c)
        speak(output)
        return output

def log_conversation(user_input, jarvis_response, log_file="conversation_log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}]\n")
        f.write(f"[User]: {user_input}\n")
        f.write(f"[jarvis]: {jarvis_response}\n")


#Main Function:
if __name__ == "__main__":  #All below codes will only run if it is executed through the main file(current file).
    speak("Initializing Jarvis")
    #Listen to wake word "jarvis"
    while True:
            r = sr.Recognizer()
            with sr.Microphone(device_index=2) as source:  #Obtain audio from microphone , Normal(laptop mic) is not working so we are using 'Microphone (Realtek(R) Audio)' so device_index = 2.
                r.adjust_for_ambient_noise(source, duration=1)  #This helps the recognizer ignore background noise(Background Filter)
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=4)  #Timeout=5(This sets the maximum time to wait for the user to start speaking. If no speech is detected in 5 seconds, it raises a WaitTimeoutError....)phrase_time_limit=10(This limits the duration of speech after the user starts talking.The recognizer will automatically stop recording after 10 seconds.)
            print("Recognizing...")
            try:
                word = r.recognize_google(audio, language='en-IN')   #This takes audio as input and try to recognize what user has asked or given as input for more better i have used language='en-IN' it say that the language speak by user is english(india).
                print(word)
                if difflib.get_close_matches("jarvis", word.lower().split()):   #Say "jarvis" and get a voice saying "Ya"
                    speak("Ya")

                    #Listen for command:
                    with sr.Microphone(device_index=2) as source:
                        r.adjust_for_ambient_noise(source)
                        print("jarvis Active...")
                        audio = r.listen(source, timeout=2, phrase_time_limit=4)
                        command = r.recognize_google(audio, language='en-IN')
                        print(command)

                        b = processCommand(command)
                log_conversation(command, b)
                with open("test.wav", "wb") as f:  #We open a new file in wb mode(write binary-needed because audio data is binary, not text).
                    f.write(audio.get_wav_data())  #It returns the raw audio data in WAV format (a standard uncompressed audio format) in simple terms we store the user data/ask in audio format in a file name test.wav .
            except sr.WaitTimeoutError:            #This occur if our AI does not receive any input from user and through timeout error.
                print("Timeout: No speech detected.")
            except Exception as e:
                print(f"Error {e}")