#!/usr/bin/env python
# coding=utf-8
"""Python Editor dynamic menu."""

import sys

import class_lib
import funct_lib
import lib
import var_lib

# TODO: Easy map (pathway) through the logic...
# TODO: More Conversational dialogue
# TODO: Better current status/output in each menu.
# TODO: status_updates as transient things that get overwritten.
CONTENTS = []
HEADER = '''#!/usr/bin/env python
# coding=utf-8

"""This is a placeholder module docstring."""

'''
OUTFILE = './no_name.py'
SETTINGS = lib.get_settings()


@lib.not_implemented
def change_log_level():
    """Change the logging level."""
    pass


def create_menu():
    """Run the 'create' menu."""
    menu_opts = {
        'Create a new function': {'action': funct_lib.create_function, 'keyword': 'function'},
        'Create a new class': {'action': class_lib.create_class, 'keyword': 'class'},
        'Create a new variable': {'action': var_lib.create_variable, 'keyword': 'variable'},
    }
    results = lib.run_menu('Create', menu_opts)
    CONTENTS.extend(results)


def change_outfile():
    """Change the OUTFILE to store results in."""
    filename = lib.get_user_input('What would you like to name the output file?')
    global OUTFILE
    OUTFILE = filename + '.py'


@lib.not_implemented
def edit_menu():
    """Run the 'edit' menu."""
    pass


@lib.not_implemented
def delete_menu():
    """Run the 'delete' menu."""
    pass


def save():
    """Save the current project and its functions/classes/variables, etc."""
    lib.status_update('Saving progress.')
    with open(OUTFILE, 'w+') as wfile:
        # TODO: More intelligence here, so we don't overwrite stuff.
        wfile.writelines(HEADER + '\n'.join(CONTENTS))


def save_and_exit():
    """Run the 'save and exit' menu."""
    if lib.get_yes_or_no('Do you want to save before you exit?'):
        save()
    lib.status_update('Good bye.')
    sys.exit(0)


def settings_menu():
    """Run the 'settings' menu."""
    menu_opts = {
        'Change the output file': {'action': change_outfile, 'keyword': 'file'},
        'Change the logging level': {'action': change_log_level, 'keyword': 'log'},
        'Enable/Disable validation': {'action': toggle_validation, 'keyword': 'validation'},
        # TODO: Modify the header.
        # TODO: Modify the imported modules.
        # TODO: Change the voice.
        # TODO: Change the language.
        # TODO: Toggle on/off always display choices.
    }
    # TODO: Update the existing settings.ini file with the new setting.
    lib.run_menu('Settings', menu_opts)


def toggle_validation():
    """Enable/Disable validation prompts."""
    if SETTINGS['logic']['validation'] == 'True':
        SETTINGS['logic']['validation'] = 'False'
    else:
        SETTINGS['logic']['validation'] = 'True'


def main():
    """Run the main menu."""
    menu_opts = {
        'Create a new object': {'action': create_menu, 'keyword': ['create', 'new']},
        'Edit an object': {'action': edit_menu, 'keyword': 'edit'},
        'Delete an object': {'action': delete_menu, 'keyword': 'delete'},
        'Settings': {'action': settings_menu, 'keyword': 'settings'},
        'Save': {'action': save, 'keyword': 'save'},
        'Exit': {'action': save_and_exit, 'keyword': 'exit'},
    }
    lib.run_menu('Main', menu_opts)


if __name__ == '__main__':
    main()
