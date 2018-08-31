# coding=utf-8
"""Helper functions for running listening tasks."""

import nltk
import pyttsx3
import speech_recognition


def echo() -> None:
    """Listen for input and then repeat what was said."""
    input_text = listen_and_transcribe(interpret=False)
    if input_text:
        status_update('I will now repeat back what you said.')
        status_update(input_text)
    else:
        status_update('Nothing was said, so I have nothing to repeat.')


def listen_and_transcribe(interpret=True) -> str:
    """Listen to mic audio and convert to text.

    Arguments:
        interpret (bool): Try to interpret the meaning; don't just pass through the exact text.

    Returns:
        result (str): The interpreted text from the audio input.
    """
    rec = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        try:
            audio_data = rec.listen(source, timeout=3)
            # TODO: Why does this sometimes not hear the first few word(s)?
        except speech_recognition.WaitTimeoutError:
            audio_data = ''
    if not audio_data:
        status_update('I didn\'t hear anything, please try again.')
        result = ''
    else:
        try:
            result = rec.recognize_google(audio_data)
        except Exception as err:
            print(err)
            status_update('I didn\'t understand what was said.  Please try again.')
            return listen_and_transcribe(interpret=interpret)
    if interpret and result:
        result = interpret_meaning(result)
    return result


def interpret_meaning(text: str) -> str:
    """Try to interpret the 'meaning' of what was said.  Translate it into a known term if applicable."""
    print('Analyzing text: {}.'.format(text))
    status_update('Let me see if I understand.')
    # Break up the "sentence" into individual tokens (bigrams for now).
    tokens = nltk.word_tokenize(text)
    # Remove any stop words which don't really help the context.
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]
    # Simplify words down to their roots/stems; in this case Porter Stemming so we have an actual word.
    stemmer = nltk.stem.PorterStemmer()
    stems = [stemmer.stem(token) for token in tokens]
    if not stems:
        status_update('I wasn\'t able to figure out what you meant.')
        result = ''
    else:
        result = ' '.join(stems)
    return result


def speak_text(text: str) -> None:
    """Speak text back to the user.

    Arguments:
        text (str): Text to vocalize.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def status_update(msg: str):
    """Provide a verbal and visual status update."""
    print(msg)
    speak_text(msg)
