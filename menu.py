#!/usr/bin/env python3
# coding=utf-8
"""An interactive menu which relies upon audio commands and options."""

import listener
import re
import sys


def status_update(msg: str):
    """Provide a verbal and visual status update."""
    print(msg)
    listener.speak_text(msg)


class Menu(object):
    """Base class for menus."""
    sub_menus = []

    def __init__(self, menu_name: str, choices: list):
        self.choices = sorted(choices + ['go back', 'exit'])
        self.name = menu_name.lower().strip()
        self.previous_menu = None

    def __repr__(self):
        return '<{}: "{}">'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return 'Then "{}" menu.'.format(self.name)

    def get_help(self):
        """Display help... aka available choices."""
        msg = 'The available choices are: {}'.format(' '.join(self.choices))
        status_update(msg)

    def get_user_input(self, prompt='Please make a selection.', interpret=True):
        """Get verbal user input.

        Arguments:
            prompt (str): What to prompt/question to ask the user.
            interpret (bool): Whether to interpret the input via NLTK or keep it raw.

        Return:
            text (str): The text interpretation of the verbal input.
        """
        listener.speak_text(prompt)
        raw_text = listener.listen_and_transcribe(interpret=interpret)
        text = raw_text.lower().strip()
        return text

    def go_back(self):
        """Go back to the previous menu."""
        if self.previous_menu:
            self.previous_menu.run_menu()
        else:
            status_update('No previous menu exists.')

    def exit(self):
        """Exit the menu."""
        status_update('Exiting')
        sys.exit(0)

    def run_menu(self):
        """Run the current menu."""
        status_update('Welcome to the {}.'.format(self.name))
        while True:
            matched = False
            self.get_help()
            text = re.sub(r'\s+', '_', self.get_user_input())
            status_update(text)
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
                status_update('I didn\'t find any matches.  Please try again.')
            else:
                status_update('Is there anything else that I can help you with?')
