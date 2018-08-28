"""Helper functions for running listening tasks."""

import speech_recognition


def listen_and_transcribe():
    """Listen to mic audio and convert to text."""
    rec = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        audio_data = rec.listen(source)
    try:
        result = rec.recognize_google(audio_data)
    except Exception as err:
        print(err)
        print('The API was unreachable or the input was unintelligible.')
        result = ''
    return result
