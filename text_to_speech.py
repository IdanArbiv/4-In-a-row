import os

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import pygame

def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, tld='co.il')
    tts.save("output.mp3")
    # os.system("start output.mp3")  # for Windows

    # os.system("afplay output.mp3")  # for macOS
    # os.system("mpg321 output.mp3")  # for Linux

text = "Hi Ohad Ben Schahar whats going on? Im Shira your bot for Arba be shura game"
text_to_speech(text)
play_mp3("output.mp3")

