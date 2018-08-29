"""Helper functions for running listening tasks."""

import pyttsx3
import speech_recognition


def echo(timeout=5) -> None:
    """Listen for input and then repeat what was said.

    Arguments:
        timeout (int): A timeout threshold in seconds to wait for audio input.
    """
    input_text = listen_and_transcribe(timeout=timeout)
    if input_text:
        speak_text('I will now repeat back what you said.')
        speak_text(input_text)
    else:
        speak_text('Nothing was said, so I have nothing to repeat.')


def listen_and_transcribe(timeout: int) -> str:
    """Listen to mic audio and convert to text.

    Arguments:
        timeout (int): A timeout threshold in seconds to wait for audio input.

    Return:
        result (str): The interpreted text from the audio input.
    """
    rec = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        try:
            speak_text('I am now listening.')
            audio_data = rec.listen(source, timeout=timeout)
        except speech_recognition.WaitTimeoutError:
            audio_data = None
    if not audio_data:
        speak_text('I didn\'t hear anything, please try again.')
        result = ''
    else:
        try:
            result = rec.recognize_google(audio_data)
        except Exception as err:
            print(err)
            speak_text('I didn\'t understand what was said.  Please try again.')
            result = ''
    return result


def speak_text(text: str) -> None:
    """Speak text back to the user.

    Arguments:
        text (str): Text to vocalize.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
