# coding=utf-8
"""Helper functions for running listening tasks."""

import os
import re

import configparser
import nltk
import pyttsx3
import speech_recognition

REL_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(REL_DIR, 'settings.ini')
SETTINGS = configparser.RawConfigParser()
SETTINGS.read(SETTINGS_FILE)
STOP_WORDS = [word.lower().strip() for word in nltk.corpus.stopwords.words('english')]


def echo() -> None:
    """Listen for input and then repeat what was said."""
    input_text = listen_and_transcribe(interpret=False)
    if input_text:
        status_update('I will now repeat back what you said.')
        status_update(input_text)
    else:
        status_update('Nothing was said, so I have nothing to repeat.')


def get_user_input(prompt='Please make a selection now.', interpret=True, convert_spaces=False) -> str:
    """Get verbal user input.

    Arguments:
        prompt (str): What to prompt/question to ask the user.
        interpret (bool): Whether to interpret the input via NLTK or keep it raw.
        convert_spaces (bool): Convert the spaces between words to underscores.
            i.e. 'get help' -> 'get_help'

    Return:
        text (str): The text interpretation of the verbal input.
    """
    status_update(prompt)
    raw_text = listen_and_transcribe(interpret=interpret)
    text = raw_text.lower().strip()
    if convert_spaces:
        re.sub(r'\s', '_', text)
    status_update('Got it.')
    return text


def listen_and_transcribe(interpret=True, timeout=3) -> str:
    """Listen to mic audio and convert to text.

    Arguments:
        interpret (bool): Try to interpret the meaning; don't just pass through the exact text.
        timeout (int): Timeout in seconds for listening to user input.

    Returns:
        result (str): The interpreted text from the audio input.
    """
    # TODO: Replace this with something that is "always listening" for keywords.
    rec = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        while True:
            try:
                rec.adjust_for_ambient_noise(mic)
                audio_data = rec.listen(mic, timeout=timeout)
                result = rec.recognize_google(audio_data)
            except speech_recognition.WaitTimeoutError:
                status_update('I didn\'t hear anything.  Please try again.')
                continue
            except speech_recognition.UnknownValueError:
                status_update('I didn\'t understand what was said.  Please try again.')
                continue
            if interpret and result:
                result = interpret_meaning(result)
            if result:
                break
    return result


def interpret_meaning(text: str) -> str:
    """Try to interpret the 'meaning' of what was said.  Translate it into a known term if applicable."""
    status_update('Analyzing text: {}.'.format(text))
    # Break up the "sentence" into individual tokens.
    # TODO: Add support for n-gram interpretations.
    tokens = nltk.word_tokenize(text)
    # Remove any stop words which don't really help the context.
    tokens = [token for token in tokens if token.lower() not in STOP_WORDS]
    # Simplify words down to their roots/stems; in this case Porter Stemming so we have an actual word.
    stemmer = nltk.stem.PorterStemmer()
    stems = [stemmer.stem(token) for token in tokens]
    if not stems:
        status_update('I wasn\'t able to figure out what you meant.')
        result = ''
    else:
        result = ' '.join(stems)
    return result


def speak_text(text: str, voice_id=SETTINGS['voice']['id']) -> None:
    """Speak text back to the user.

    Arguments:
        text (str): Text to vocalize.
        voice_id (str): A voice ID to use instead of the default; this defaults to Apple's Samantha.
    """
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()


def status_update(msg: str):
    """Provide a verbal and visual status update."""
    print(msg)
    speak_text(msg)
