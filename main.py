import os
import sys
import json
import time
import subprocess
import pyautogui
import pyaudio
from colorama import init, Fore, Style
from vosk import Model, KaldiRecognizer, SetLogLevel

pyautogui.FAILSAFE = False

SetLogLevel(-1)

init(autoreset=True)

CONFIG_FILE = "config.json"

ASCII_ART = """
      _    _          _       _       _     _ _   
     | |  (_)        | |     | |     | |   (_) |  
  ___| | ___ _ __  __| | __ _| |_ ___| |__  _| |_ 
 / __| |/ / | '_ \/ _` |/ _` | __/ __| '_ \| | __|
 \__ \   <| | |_) | (_| | (_| | |_\__ \ | | | | |_ 
 |___/_|\_\_| .__/ \__,_|\__,_|\__|___/_| |_|_|\__|
            | |                                   
            |_|                                   
"""

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + Style.BRIGHT + ASCII_ART)
    print(Fore.YELLOW + "github.com/coolerts")
    print(Fore.YELLOW + "скипает рекламу по твоему слову\n")

def skip_youtube_ad(x, y):
    current_x, current_y = pyautogui.position() 
    pyautogui.moveTo(x, y, duration=0.0)
    pyautogui.click()
    pyautogui.moveTo(current_x, current_y, duration=0.0) 
    print(Fore.YELLOW + f"[инфа] кликнул на ({x}, {y})")

def run_assistant():
    config = load_config()
    click_x = config.get("click_x")
    click_y = config.get("click_y")
    trigger = config.get("trigger_word", "выключи")

    if click_x is None or click_y is None:
        print(Fore.RED + "[еррор] ты корды не задал дупло")
        input(Fore.YELLOW + "enter для меню")
        return

    print(Fore.YELLOW + "[инфо] гружу нейронку для распознания твоего голоска")
    
    model = Model(lang="ru")
    
    grammar = f'["{trigger}", "[unk]"]'
    recognizer = KaldiRecognizer(model, 16000, grammar)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print_header()
    print(Fore.YELLOW + "[инфо] запущен")
    print(Fore.YELLOW + f"[инфо] скажи {trigger} чтоб рекламу скипнуть")
    print(Fore.YELLOW + "[инфо] просто закрой окно чтобы вырубить прогу")

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if trigger in text:
                    print(Fore.YELLOW + "[!] понял принял, скипаю")
                    skip_youtube_ad(click_x, click_y)
                    time.sleep(1.5)
                    recognizer.Reset()

    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def main_menu():
    while True:
        config = load_config()
        trigger = config.get("trigger_word", "выключи")
        
        print_header()
        print(Fore.YELLOW + "команды:")
        print(Fore.YELLOW + "1. выбрать область кнопки скипа рекламы")
        print(Fore.YELLOW + "2. запуск проги")
        print(Fore.YELLOW + f"3. изменить слово-триггер (сейчас: {trigger})")
        print(Fore.YELLOW + "4. выход")

        choice = input(Fore.YELLOW + "\nпиши: ")

        if choice == '1':
            print(Fore.YELLOW + "[инфо] выделения")
            subprocess.run([sys.executable, "selector.py"])
        elif choice == '2':
            run_assistant()
        elif choice == '3':
            new_word = input(Fore.YELLOW + "введи новое слово: ").strip().lower()
            if new_word:
                config["trigger_word"] = new_word
                save_config(config)
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit(0)
        else:
            print(Fore.RED + "че за хуйню ты мне дал")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
