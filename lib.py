# coding=utf-8
"""Common library of helpers for listening, interpreting input, speaking, etc."""

import itertools
import logging
import os
import re

import configparser
import nltk
import pyttsx3
import speech_recognition

# TODO: Add support for other languages besides en-US.
LOGGER = logging.getLogger('parsel_tongue')
REL_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(REL_DIR, 'settings.ini')
SETTINGS = configparser.RawConfigParser()
SETTINGS.read(SETTINGS_FILE)
STEMMER = nltk.stem.PorterStemmer()
STOP_WORDS = [word.lower().strip() for word in nltk.corpus.stopwords.words('english')]
VOICE_ENGINE = pyttsx3.init()
VOICE_ENGINE.setProperty('voice', SETTINGS['voice']['voice_id'])


def _delete_line():
    """Delete a logic line."""
    pass


def _edit_line():
    """Edit a logic line."""
    pass


def _new_line():
    """Create a new logic line."""
    # TODO: Logic add menu for common things and interactivity beyond just raw speech.
    # Things like: add an operator, add a variable, etc.
    logic_line = get_user_input('What logic do you want to add?')
    return logic_line


def create_logic_lines(tab_level=1) -> str:
    """Create individual logic lines for a function/method/etc."""
    # TODO: How to display current context in the run_menu, pass in results?
    choices = {
        'Add a new line': {'action': _new_line, 'keyword': 'new'},
        'Edit a line': {'action': _edit_line, 'keyword': 'edit'},
        'Delete a line': {'action': _delete_line, 'keyword': 'delete'},
    }
    raw_lines = run_menu('Logic Lines', choices)
    # TODO: Support custom indentation levels for each line...
    tabbed_lines = [('    ' * tab_level) + line for line in raw_lines]
    lines = '\n'.join(tabbed_lines)
    return lines


def generate_keywords(action_words: list) -> dict:
    """For the given action words, e.g. 'delete', create a list of words of equivalent meaning."""
    keywords = {}
    for a_word in action_words:
        # Get synonyms, if none exist, then just use the original word.
        s_words = get_synonymns(a_word) or [a_word]
        # Generate stems of the synonyms.
        keywords[a_word] = [STEMMER.stem(s_word) for s_word in s_words]
    return keywords


def get_choice(prompt: str, choices: dict) -> str:
    """Get the user's input until it matches one of the available choices."""
    # Remove duplicates and lower/strip them for easier matching.
    result = ''

    # Generate a list of synonymous word stems of the given keyword.
    for choice, config in choices.items():
        keywords = config['keyword']
        if isinstance(keywords, str):
            keywords = [keywords]
        choices[choice]['stems'] = generate_keywords(keywords)

    # Keep trying until there is a result which matches the available choices.
    while not result:
        choices_text = sorted(choices.keys())
        user_response = get_user_input(prompt, choices_text)
        # Get the user response by index, instead of by text matching.
        if user_response.isdigit():
            result = choices_text[int(user_response) - 1]
        else:
            for stemmed_word in parse_text(user_response).split():
                for choice, config in choices.items():
                    for root_word, stems  in config['stems'].items():
                        if stemmed_word in stems:
                            result = choice
                            break
                    if result:
                        break
                if result:
                    break
            if not result:
                status_update('I wasn\'t able to match any of the available options. Please try again.')
    status_update('You selected "{}".'.format(result))
    if SETTINGS['logic']['validation'] == 'True' and not get_yes_or_no('Is that correct?'):
        result = get_choice(prompt, choices)
    return result


def get_help(options: list):
    """Display help for the current options."""
    opts = []
    for index, option in enumerate(sorted(list(options))):
        # Example: "1) Create a new function"
        opt = '{}) {}.'.format(index + 1, option)
        opts.append(opt)
    # TODO: Make this speech more natural here.
    status_update('\n'.join(opts))
    return opts


def get_settings():
    """Get global settings."""
    settings = configparser.RawConfigParser()
    settings.read(SETTINGS_FILE)
    return settings


def get_synonymns(text: str) -> list:
    """Get words which are synonymous with another word."""
    synonyms = nltk.corpus.wordnet.synsets(text)
    possible_matches = set(itertools.chain.from_iterable([item.lemma_names() for item in synonyms]))
    return list(possible_matches)


def get_user_input(prompt='Please make a selection now.', choices=None, interpret=True, convert_spaces=False) -> str:
    """Get verbal user input.

    Arguments:
        prompt (str): What to prompt/question to ask the user.
        choices (list): Optional list of choices which should be presented to the user.
        interpret (bool): Whether to interpret the input via NLTK or keep it raw.
        convert_spaces (bool): Convert the spaces between words to underscores.
            i.e. 'get help' -> 'get_help'

    Return:
        text (str): The text interpretation of the verbal input.
    """
    status_update(prompt)
    if choices:
        get_help(choices)
    raw_text = listen_and_transcribe(interpret=interpret)
    text = raw_text.lower().strip()
    if convert_spaces:
        re.sub(r'\s', '_', text)
    return text


def get_yes_or_no(prompt='Please say "yes" or "no".') -> bool:
    """Prompt the user for a 'yes' or 'no' response."""
    response = get_user_input(prompt, interpret=False)
    LOGGER.debug('Raw response: "{}".'.format(response))
    like_yes = get_synonymns('yes')
    like_no = get_synonymns('no')
    if response in like_yes:
        response = 'yes'
    elif response in like_no:
        response = 'no'
    else:
        status_update('I didn\'t understand what you said.')
        response = str(get_yes_or_no())
    LOGGER.debug('The parsed response was: "{}".'.format(response))
    return 'yes' in response


def get_text_input(interpret=True, **kwargs) -> str:
    """Get text input from the user."""
    result = str(input('Please enter your response: '))
    if interpret:
        result = interpret_meaning(result)
    return result


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
        rec.adjust_for_ambient_noise(mic)
        while True:
            try:
                # TODO: Have some sort of indicator here that it is now listening!
                print('\a')
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
    # Break up the "sentence" into individual tokens.
    # TODO: Add support for n-gram interpretations.
    tokens = nltk.word_tokenize(text)
    # Remove any stop words which don't really help the context.
    tokens = [token for token in tokens if token.lower() not in STOP_WORDS]
    # Simplify words down to their roots/stems; in this case Porter Stemming so we have an actual word.
    stems = [STEMMER.stem(token) for token in tokens]
    if not stems:
        status_update('I wasn\'t able to figure out what you meant.')
        result = ''
    else:
        result = ' '.join(stems)
    return result


def parse_text(text: str) -> str:
    """Parse user input text via NLP."""
    # Break up the "sentence" into individual tokens.
    # TODO: Add support for n-gram interpretations.
    tokens = nltk.word_tokenize(text)
    # Remove any stop words which don't really help the context.
    tokens = [token for token in tokens if token.lower() not in STOP_WORDS]
    # Simplify words down to their roots/stems; in this case Porter Stemming so we have an actual word.
    stems = [STEMMER.stem(token) for token in tokens]
    if not stems:
        result = ''
    else:
        result = ' '.join(stems)
    return result


def not_implemented(funct):
    """Does not run the sub-function, but simply returns that it is not implemented."""
    LOGGER.warning('"{}" was called, but is not implemented yet.'.format(funct.__name__))
    return lambda: status_update('This feature is not yet implemented.')


def run_menu(title: str, options: dict, display=None, **kwargs) -> list:
    """Run a menu with the given title and options.

    Arguments:
        title (str): The title of the menu.
        options (dict): Options for navigation in the menu.
            This should include the text to display, a keyword, and a function to run/action to take.
            Example: {'Start a new project': 'keyword': 'new', 'action': new_project}
        display (str): Optional display to include in the menu output.

    Returns:
        results (str): The result of the action taken, based upon the user's input.
    """
    if not display:
        display = ''
    if not title.endswith('Menu'):
        title += ' Menu'
    LOGGER.debug('Starting the {} menu.'.format(title))
    status_update('{}.'.format(title))
    results = []
    while True:
        os.system('clear')  # Clear out any previous text.
        print(display)
        choice = get_choice('Please choose one of the following:', options)
        action = options[choice]['action']
        if not action:
            LOGGER.warning('User choice "{}" had no matches.'.format(choice))
            status_update('The choice you selected does not exist.')
            continue
        else:
            # Run the action:
            status_update('Okay.')
            result = action(**kwargs)
            results.append(result)
            if result:
                display += result + '\n'
            # Determine if anything else is needed.
            if get_yes_or_no('{}.  Do you want to do anything else?'.format(title)):
                continue
            else:
                status_update('Closing the {}.'.format(title))
                break
    return results


def simple_prompt(prompt: str, interpret=False) -> str:
    """Get the requested description."""
    response = get_user_input(prompt, interpret=interpret)
    status_update('You said: "{}".'.format(response))
    if SETTINGS['logic']['validation'] == 'True' and not get_yes_or_no('Is that correct?'):
        response = simple_prompt(prompt, interpret)
    return response


def speak_text(text: str) -> None:
    """Speak text back to the user.

    Arguments:
        text (str): Text to vocalize.
    """
    VOICE_ENGINE.say(text)
    VOICE_ENGINE.runAndWait()


def status_update(msg: str):
    """Provide a verbal and visual status update."""
    LOGGER.debug(msg)
    print(msg)
    speak_text(msg)


