import speech_recognition as sr
import os
from mtranslate import translate
from colorama import Fore, Style, init

init(autoreset=True)

def print_loop():
    while True:
        print(Fore.LIGHTGREEN_EX)


def Trans_hindi_to_english(txt):
    """Translate Hindi to English."""
    english_txt = translate(txt, to_language='en-in')
    return english_txt


def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3500
    recognizer.dynamic_energy_threshold = False
    recognizer.dynamic_energy_adjustment_damping = 0.03
    recognizer.dynamic_energy_ratio = 1.9
    recognizer.pause_threshold = 0.4
    recognizer.operation_timeout = None
    recognizer.non_speaking_duration = 0.1
    recognizer.phrase_threshold = 0.2

    # List available microphones
    # mic_list = sr.Microphone.list_microphone_names()
    # print("Available microphones:")
    # for i, mic_name in enumerate(mic_list):
    #     print(f"{i}: {mic_name}")

    #mic_index = int(input("Enter the index of your microphone: "))  # Update this index accordingly
    mic_index = 2

    # Use the selected microphone
    with sr.Microphone(device_index=mic_index) as source:

        recognizer.adjust_for_ambient_noise(source)

        print(Fore.LIGHTGREEN_EX + "Listening for your command...", end="", flush=True)

        try:
            # Listen for audio input with a timeout of 5 seconds
            audio = recognizer.listen(source, timeout=5)
            print("\r" + Fore.LIGHTGREEN_EX + "Got it! Now to recognize it...", end="", flush=True)

            # Recognize speech using Google's speech recognition
            recognized_txt = recognizer.recognize_google(audio).lower()

            if recognized_txt:
                print(f"\r{Fore.BLUE}tejas: {recognized_txt}")
                translated_txt = Trans_hindi_to_english(recognized_txt)
                print("\r" + Fore.BLUE + "Translated: " + translated_txt)
                return translated_txt
            else:
                return ""

        except sr.UnknownValueError:
            print("\r" + Fore.RED + "Sorry, I couldn't understand what you said.")
        except sr.WaitTimeoutError:
            print("\r" + Fore.RED + "Listening timed out. Please speak again.")
        except sr.RequestError:
            print("\r" + Fore.RED + "There was an issue with the Google Speech Recognition service.")
        except KeyboardInterrupt:
            print("\r" + Fore.RED + "Program interrupted. Exiting...")

