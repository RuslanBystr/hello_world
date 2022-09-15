from settings import *
from API import (currency, news, weather, wiki)

import webbrowser as wb
import os
import sys

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config

from speech_recognition import Microphone, RequestError, Recognizer, UnknownValueError
from fuzzywuzzy import fuzz
import keyboard
import pyttsx3
import sqlite3


speak_engine = pyttsx3.init()


volume = 0.5
convers_speed = 185


def voice_instalation():
    """If you not have synthesized voice"""

    voice_not_found = True

    for v in speak_engine.getProperty('voices'):
        if v.name == "Volodymyr":
            # os.remove("RHVoice-voice-Ukrainian-Volodymyr-v4.0.1011.14-setup.exe")
            voice_not_found = False
    if voice_not_found:
        os.system("RHVoice-voice-Ukrainian-Volodymyr-v4.0.1011.14-setup.exe")


voice_instalation()

rec = Recognizer()
micro = Microphone()

def speak(text):
    print(text)
    speak_engine.setProperty('voice', VOICE_ID)
    speak_engine.setProperty("volume", volume)
    speak_engine.setProperty("rate", convers_speed)
    speak_engine.say(text)
    speak_engine.runAndWait()
    speak_engine.stop()
    return text


def voice_to_txt(voice):

    text = rec.recognize_google(voice, language=REC_LANG).lower()
    return text


class Assistant:
    """
    it's voice assistant. He is very cool
    """

    def __init__(self, name):
        self.name = name


    def cmd_call(self, instance):
        try:
            with micro as source:
                print("Скажіть щось ...")
                audio = rec.listen(source)

            self.text = voice_to_txt(audio)
            app.setText(self.text, "right")
            text_cmd = self.recognize_cmd()
            app.setText(text_cmd, "left")

        except UnknownValueError:
            app.setText("Голос не розпізнано!", "left")
            speak("Я вас не почув!")

        except RequestError:
            app.setText("Перевірте підключення до мережі!", "left")

    def recognize_cmd(self) -> str:

        DATA_BASE = sqlite3.connect('database/commands.db', check_same_thread=False)
        sql = DATA_BASE.cursor()
        words = self.text.split(" ")

        for elem in words:
            if elem == "кажу":
                self.text = self.text.replace(elem, "")
            if elem in ALIAS:
                self.text = self.text.replace(elem, "")

        if self.text.startswith(" "):
            del self.text[0]
        if self.text.endswith(" "):
            del self.text[-1]

        for cmd in sql.execute("SELECT * FROM execute_cmd"):
            if fuzz.ratio(self.text, elem[0]) > 80:
                # print("Схожість команди: " + str(fuzz.ratio(self.text, elem[0]))+"%")
                CmdFunctions.func_call(elem[1])
                return "Виконано"

        for cmd in sql.execute("SELECT * FROM URL"):
            if fuzz.ratio(self.text, elem[0]) > 80:
                # print("Схожість команди: " + str(fuzz.ratio(self.text, elem[0]))+"%")
                wb.open(elem[1])
                speak("Виконав")
                return "Виконав"

        for cmd in sql.execute("SELECT * FROM questions"):
            if fuzz.ratio(self.text, elem[0]) > 85:
                print("Схожість команди: " + str(fuzz.ratio(self.text, elem[0]))+"%")
                speak(elem[1])
                return elem[1]

        return speak("Я вас не зрозумів")


class CmdFunctions:

    @staticmethod
    def func_call(cmd):
        for key, value in EXEC_CMDS.items():
            if cmd == key:
                print(exec(value))

                break

    @staticmethod
    def _search_in_wiki():
        speak("що вас цікавить?")
        try:
            with micro as source:
                audio = rec.listen(source, phrase_time_limit=5)
            request = voice_to_txt(audio)
            speak(wiki.get_wiki(request))

        except UnknownValueError:
            speak("Я вас не почув!")

    @staticmethod
    def _write():
        speak("я вас слухаю:")
        with micro as source:
            source = rec.listen(source)
            write_txt = voice_to_txt(source)
        keyboard.write(write_txt)

    @staticmethod
    def _now_time():
        zero = ""
        if NOW_TIME.minute < 10:
            zero = "0"
        time = "Зараз: " + str(NOW_TIME.hour) + ":" + zero + str(NOW_TIME.minute)
        speak(str(time))
        return time

    @staticmethod
    def _now_weather():
        speak("Зараз " + weather.get_weather(weather.LOCATE, weather.WEATHER_TOKEN))

    @staticmethod
    def _news():
        speak(news.news())
        return "Новини"

    @staticmethod
    def _get_dolar():
        return speak(currency.get_currency('USD'))

    @staticmethod
    def _get_euro():
        return speak(currency.get_currency('EUR'))

    @staticmethod
    def _calculate():
        speak("кажіть")
        with micro as source:
            source = rec.listen(source)
            text = voice_to_txt(source)
        try:
            list_of_varible = ["", ""]
            i = 0
            for digit in text:
                if digit == " ":
                    continue
                if digit == "+":
                    i += 1
                    continue

                list_of_varible[i] += digit
            list_ints = list(map(int, list_of_varible))
            result = speak("це буде: " + str(sum(list_ints)))
        except:
            result = speak("Неправильно заданий приклад")
        return result

    @staticmethod
    def volume_up(_):
        speak("окі чпокі")
        global volume
        if volume <= 1.0:
            volume += .1
            volume = float('{:.2f}'.format(volume))
        else:
            volume = 1
        return str(volume * 100) + "%"

    @staticmethod
    def volume_down(_):
        global volume
        if volume > 0:
            volume -= .1
            volume = float('{:.2f}'.format(volume))
        else:
            volume = 0
        return str(volume * 100) + "%"
   
    @staticmethod
    def _speak_faster():
        global convers_speed
        convers_speed += 15
        speak("добре")
        return convers_speed

    @staticmethod
    def _speak_slower():
        global convers_speed
        convers_speed -= 15
        speak("добре")
        return convers_speed

    @staticmethod
    def _exit():
        time_of_farewell = ""
        if NOW_TIME.hour in [h for h in range(4, 18)]:
            time_of_farewell = "ще побачимось"
        elif NOW_TIME.hour > 18 and NOW_TIME.hour < 22:
            time_of_farewell = "бувайте"
        else:
            time_of_farewell = "доброї ночі"
        speak(time_of_farewell)
        sys.exit()


def greeting():
    n_minute = NOW_TIME.minute
    time_of_greeting = "добрий день"
    if NOW_TIME.hour in [h for h in range(4, 11)]:
        time_of_greeting = "доброго ранку"
    elif NOW_TIME.hour > 11 and NOW_TIME.hour < 18:
        time_of_greeting = "добрий день"
    elif NOW_TIME.hour > 18:
        time_of_greeting = "добрий вечір"

    if n_minute < 10:
        n_minute = str("0" + str(NOW_TIME.minute))

    speak(f"""{time_of_greeting}. Вас вітає {NAME}. Зараз
        {NOW_TIME.hour}:{"0" + str(n_minute) if n_minute < 10 else str(n_minute)},
        на вулиці {weather.get_weather("Lutsk", weather.WEATHER_TOKEN)} 
        """)


Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 400)


class WindowAssistantApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical", padding=20)
        self.gl = GridLayout(cols=3, spacing=3)

        self.init_buts =[Label(text="", halign="left", valign="bottom", text_size=(400 - 40, 15),
                         size_hint=(1, .3), font_size=16) for _ in range(10)]


        self.b1 = Button(text="V-",
                         on_press=CmdFunc.volume_down,
                         border=(10, 10, 10, 10),
                         size_hint=(1, .4),
                         font_size=46)
        self.b2 = Button(on_press=Assist.cmd_call,
                         background_normal="images/microphone.jpg",
                         border=(10, 10, 10, 10),
                         size_hint=(1, .4))
        self.b3 = Button(text="V+",
                         on_press=CmdFunc.volume_up,
                         border=(10, 10, 10, 10),
                         size_hint=(1, .4),
                         font_size=46)

    def setText(self, text, halign="left"):

            
        self.init_buts[-1].text, self.init_buts[-1].halign = text, halign   
        

    def build(self):
        self.title = "Dima Assistant"
        self.icon = 'microphone.jpg'

        for elem in self.init_buts:
            self.bl.add_widget(elem)

        self.gl.add_widget(self.b1)
        self.gl.add_widget(self.b2)
        self.gl.add_widget(self.b3)

        self.bl.add_widget(self.gl)

        return self.bl


if __name__ == '__main__':
    Assist = Assistant(NAME)
    CmdFunc = CmdFunctions()
    app = WindowAssistantApp()
    #greeting()
    app.run()
