import speech_recognition as sr
import pyttsx3
import random
import time


def get_words():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    #r.recognize_sphinx(audio))
    return r.recognize_google(audio)


def say(words):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice = [v for v in voices if v.name == 'Karen'][0]
    print(voice.name)
    # changes the voice
    engine.setProperty('voice', voice.id)
    engine.say(f'{words}')
    engine.runAndWait()


def main():
    while True:
        words = get_words()
        print(f'You said {words}')
        say(words)


main()
