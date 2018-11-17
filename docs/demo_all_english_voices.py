import pyttsx3
import random
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(len(voices))
random.shuffle(voices)
target_langs = set(['en_GB', 'en_ZA', 'en_US', 'en_AU', 'en-scotland', 'en_IE', 'en_IN'])
voices = [v for v in voices if (target_langs & set(v.languages))]
for voice in voices:
    print(voice)
    engine.setProperty('voice', voice.id)  # changes the voice
    engine.say('Hello there. Nice to meet you')
    engine.runAndWait()
