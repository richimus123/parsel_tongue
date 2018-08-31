#!/usr/bin/env python3
# coding=utf-8
"""An interactive menu which relies upon audio commands and options."""

import re
import sys

import listener


class Menu(object):
    """Base class for menus."""
    sub_menus = []

    def __init__(self, menu_name: str, choices: list):
        self.choices = sorted(choices + ['go back', 'exit', 'help'])
        self.name = menu_name.lower().strip()
        if not self.name.endswith('Menu'):
            self.name += ' Menu'
        self.previous_menu = None

    def __repr__(self):
        return '<{}: "{}">'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return 'Then "{}" menu.'.format(self.name)

    def get_help(self):
        """Display help... aka available choices."""
        msg = 'The available choices are: {}'.format(', '.join(self.choices[:-1]) + ', or {}.'.format(self.choices[-1]))
        listener.status_update(msg)

    def get_user_input(self, prompt='Please make a selection now.', interpret=True, convert_spaces=False):
        """Get verbal user input.

        Arguments:
            prompt (str): What to prompt/question to ask the user.
            interpret (bool): Whether to interpret the input via NLTK or keep it raw.
            convert_spaces (bool): Convert the spaces between words to underscores.
                i.e. 'get help' -> 'get_help'

        Return:
            text (str): The text interpretation of the verbal input.
        """
        listener.status_update(prompt)
        raw_text = listener.listen_and_transcribe(interpret=interpret)
        text = raw_text.lower().strip()
        if convert_spaces:
            re.sub(r'\s', '_', text)
        return text

    def go_back(self):
        """Go back to the previous menu."""
        if self.previous_menu:
            self.previous_menu.run_menu()
        else:
            listener.status_update('No previous menu exists.')

    def exit(self):
        """Exit the menu."""
        listener.status_update('Exiting')
        sys.exit(0)

    def run_menu(self, ignore_words=()):
        """Run the current menu."""
        listener.status_update('Welcome to the {}.'.format(self.name))
        self.get_help()
        while True:
            matched = False
            text = self.get_user_input(convert_spaces=True)
            for word in ignore_words:
                text.replace(word, '')
            text = text.replace(' ', '_')
            listener.status_update('What I interpreted from what you said was: {}'.format(text))
            # Option 1: Easy Match; A piece of the input matches one of the methods we have defined.
            if hasattr(self, text):
                getattr(self, text)()
                matched = True
            else:
                # Option 2: Close; A piece of the input is "close to" one of the methods we have defined
                # TODO: This also needs to consider stemmed words...
                # TODO: Have a mapping of "close to the right answer" answers.
                # TODO: POS tagging to get the correct interpretation.
                # TODO: Tensorflow/Neural Network to improve accuracy of interpretations.
                for token in text:
                    if hasattr(self, token):
                        matched = True
                        getattr(self, token)()
                        break
            if not matched:
                # Option 3: Bad input; It doesn't match anything we have defined.
                listener.status_update('I didn\'t find any matches.  Please try again.')
            else:
                listener.status_update('Is there anything else that I can help you with?')
                # TODO: yes/no helper here which will call exit if 'no' in this instance.
