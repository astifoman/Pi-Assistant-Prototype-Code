from phue import Bridge
import logging
import random
from datetime import datetime
import time
import speech_recognition as sr

logging.basicConfig()
b = Bridge('192.168.0.246')

def turn_on_lights():
    b.set_light(2, 'on', True)
    b.set_light(3, 'on', True)
    change_lights_color()  # Change color immediately after turning on the lights

def turn_off_lights():
    b.set_light(2, 'on', False)
    b.set_light(3, 'on', False)

def change_lights_color():
    x = random.random()
    y = random.random()
    transition_time = 0

    b.set_light(2, 'xy', [x, y], transitiontime=transition_time)
    b.set_light(3, 'xy', [x, y], transitiontime=transition_time)

def is_nighttime():
    now = datetime.now()
    current_time = now.time()
    # Define the nighttime range, for example, between 10 PM and 6 AM
    nighttime_start = datetime.strptime('22:00', '%H:%M').time()
    nighttime_end = datetime.strptime('06:00', '%H:%M').time()

    if nighttime_start <= current_time or current_time <= nighttime_end:
        return True
    else:
        return False

def activate_lights():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something to activate the lights...")

        while True:
            audio = r.listen(source)

            try:
                # Use the Google Web Speech API for speech recognition
                text = r.recognize_google(audio)
                print("Recognized:", text)

                if "turn on" in text:
                    turn_on_lights()
                elif "turn off" in text:
                    turn_off_lights()
                else:
                    print("Sorry, I didn't understand the command.")

            except sr.UnknownValueError:
                print("Sorry, I could not understand audio.")
            except sr.RequestError as e:
                print("Sorry, could not request results from the service; {0}".format(e))

if __name__ == "__main__":
    while True:
        if is_nighttime():
            activate_lights()
        else:
            turn_off_lights()

        # Sleep for some time before checking the time again
        time.sleep(600)  # Sleep for 10 minutes
