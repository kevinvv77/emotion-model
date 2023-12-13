import time

from furhat_remote_api import FurhatRemoteAPI
import json
import numpy as np
from emotionDetection import detect_emotions

furhat: FurhatRemoteAPI = FurhatRemoteAPI("Localhost")
voices = furhat.get_voices()
furhat.set_voice(name='Matthew')
log_file = open("log.txt", "w")

with open("script.json") as file:
    script = json.load(file)


def log_data(data):
    log_file.write(data)


def start():
    introduction()
    show_random_emotion()
    furhat.say(text="Let's do one more", blocking=True)
    show_random_emotion()
    furhat.say(text="Lets proceed with the videos", blocking=True)
    show_video()
    furhat.say(text="Let's do one more", blocking=True)
    show_video()

    furhat.say(text="We are almost at the end of this experiment. Thank you for participating! my colleague will have "
                    "a few quick questions about working with me and then we'll be all set.")


def stop():
    furhat.say(text="Shutting down")


def introduction():
    furhat.say(text="Hello, I’m the furhat robot. It is very nice to meet you and thank you for participating in this "
                    "research. As the furhat robot I’m one of the most advanced social robots out there. My team and "
                    "I would like to see how accurate I can detect your emotions by reading your facial expressions. "
                    "Today I will be showing you two videos and I would like you to react to the videos how you "
                    "would normally react.",
               blocking=True)

    time.sleep(1)

    furhat.say(
        text="But first can you help by choosing one of the emotions on the template and showing this to me.",
        blocking=True)

    time.sleep(1)
    furhat.say(text="could you now please choose one emotions of the template and answer with ready when you are "
                    "ready to continue",
               blocking=True)

    proceed = False
    while not proceed:
        answer = furhat.listen()
        if answer.message.lower() == 'no':
            furhat.say(
                text="I'm sorry to hear that, let me know whenever you want to participate",
                blocking=True)
            stop()
            proceed = True
        if answer.message.lower() != 'ready':
            furhat.say(text="I didn't understand you, could you please repeat it",
                       blocking=True)
            continue
        proceed = True


def show_random_emotion():
    furhat.say(text="We will start the experiment now.",
               blocking=True)

    detected_emotions = detect_emotions(10)  # TODO: log hele dataset
    most_frequent_emotion = get_most_frequent_emotion(detected_emotions)

    validate_correct_emotion(most_frequent_emotion)


def show_video():
    furhat.say(
        text="We will now show you a video to trigger a emotion",
        lipsync=True,
        blocking=True)

    detected_emotions = detect_emotions(10)
    most_frequent_emotion = get_most_frequent_emotion(detected_emotions)

    validate_correct_emotion(most_frequent_emotion)


def validate_correct_emotion(most_frequent_emotion):
    furhat.say(
        text=f"You showed me the {most_frequent_emotion}, is that correct?",
        blocking=True)

    log_data("Guessed emotion: " + most_frequent_emotion + " ")

    while True:
        answer = furhat.listen()
        if answer.message.lower() == 'no':
            furhat.say(
                text="What emotion did you show me then?",
                blocking=True)

            correct_emotion = furhat.listen()
            log_data("Correct emotion: " + correct_emotion.message + "\n")

            furhat.say(
                text="Thank you for the feedback",
                blocking=True)

            return
        if answer.message.lower() == 'yes':
            furhat.say(text="That's great!")
            log_data("Correct emotion: " + most_frequent_emotion + "\n")
            return
        else:
            furhat.say(text="I didn't understand you, could you please repeat it",
                       blocking=True)


def get_most_frequent_emotion(detected_emotions):
    unique, counts = np.unique(detected_emotions, return_counts=True)
    index = np.argmax(counts)
    return unique[index]
