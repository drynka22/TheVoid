import speech_recognition as sr
import os
import sys
import webbrowser
import pyowm
import random
import math
import time
import pyttsx3
from colorama import init
import apiai, json
import requests
from bs4 import BeautifulSoup
import pyautogui as pg

############################################# голос и приветствие

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice','ru')

for voice in voices:
    if voice.name == 'Alyona (Russian) SAPI5':
        tts.setProperty('voice',voice.id)

tts.say('Я снова живу, я снова дышу!')
tts.runAndWait()

############################################# настройки микро

def talk(words):
    engine.say(words)

def command():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.pause_threshold = 1
        print('Говорите')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio).lower()
        print ('Вы сказали: ' + zadanie)
    except sr.UnknownValueError:
        tts.say('Ничего не поняла, но очень интересно!')
        tts.runAndWait()
        zadanie = command()
    return zadanie

############################################# 'задания'

def makeSomething(zadanie):
    if 'browser' in zadanie:
        url = 'https://yandex.ru/'
        webbrowser.open(url)
    elif 'stop' in zadanie:
        sys.exit()
    elif 'weather' in zadanie:
        owm = pyowm.OWM('324337b3700b8fcfced06055a82a4239')
        observation = owm.weather_at_place('Ярославль')
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']
        print('В Ярославле сейчас ' + w.get_status().lower())
        print('Температура сейчас в районе ' + str(temp))
    elif 'music' in zadanie:
        DIR = 'Музыка'
        try:
            os.startfile(os.path.join(DIR, random.choice(os.listdir(DIR))))
        except FileNotFoundError:
            print('Мне не удалось найти музыку :(')
        return zadanie
    elif 'bmi' in zadanie:
        init()
        weight = float(input('Ваш вес, кг?: '))
        height = float(input('Ваш рост, см?: '))
        print('')
        bmi = float('{0:.2f}'.format(weight / ((height / 100) * (height / 100))))
        print('Ваш BMI равен ' + str(bmi))
        if(bmi <=16):
            print('Высокий дефицит массы тела')
        if(bmi >=16 and bmi <= 18.5):
            print('Небольшой дефицит массы тела')
        if(bmi >= 18.5 and bmi <= 25):
            print('Ваш вес в норме')
        if(bmi >= 25 and bmi <=30):
            print('Небольшой избыток веса')
        if(bmi >=30):
            print('У вас ожирение')
    elif 'thank you' in zadanie:
        engine = pyttsx3.init()
        engine.say('Рада помочь')
        engine.runAndWait()
    elif 'turn off the computer' in zadanie:
        os.system('shutdown /s /f /t 10')
    elif 'exchange rate' in zadanie:
        DOLLAR_RUB = 'https://www.google.ru/search?newwindow=1&source=hp&ei=57VZX9CeBcWWaZb-ouAI&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQsQMQRhCCAjICCAAyCAgAELEDEIMBMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoFCAAQsQM6DAgAELEDEIMBEAoQAToNCAAQsQMQgwEQRhCCAlDnBlieKGC-LGgCcAB4AIABPogB6waSAQIxNpgBAKABAaoBB2d3cy13aXqwAQA&sclient=psy-ab&ved=0ahUKEwiQrvX-6d3rAhVFSxoKHRa_CIwQ4dUDCAc&uact=5'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        full_page = requests.get(DOLLAR_RUB, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
        print('Доллар стоит ' + convert[0].text)

        EURO_RUB = 'https://www.google.ru/search?newwindow=1&ei=6hhaX5-aCaiurgTPmYXgCQ&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIHCAAQsQMQQzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoECAAQRzoGCAAQBxAeULnWD1i46Q9ggOsPaARwA3gAgAFTiAGJA5IBATWYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwift6u1yN7rAhUol4sKHc9MAZwQ4dUDCA0&uact=5'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        full_page = requests.get(EURO_RUB, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
        print('Евро стоит ' + convert[0].text)
    elif 'screenshot' in zadanie:
        pg.screenshot('pgcreenshot.png')
    elif 'minesweeper' in zadanie:
        url = 'https://xn--80a4adb6f.com/'
        webbrowser.open(url)

while True:
    makeSomething(command())
