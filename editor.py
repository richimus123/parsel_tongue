# coding=utf-8
"""A Python editor which follows verbal commands."""

import logging
import os
import sys

import listener

# Logging:
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
HANDLER = logging.FileHandler('parsel_tongue.log')
HANDLER.setLevel(logging.INFO)
LOGGER.addHandler(HANDLER)

ADMIN_ACTIONS = {
    # Actions that should be available at any time.
    # These will not be presented to the user, but are for admin purposes.
    'Force exit': sys.exit,
    'Set Logging Level': lambda: LOGGER.setLevel(listener.get_user_input('Which logging level?'))
}
FUNCTIONS = {}
IGNORE_WORDS = [
    'function',
    'want',
    'need',
    'like',
]
LOGIC_LINES = {
    # Stored by function_name as key.
}
SETTINGS = {}  # Get these from a config file?
SYNONYMS = {
    # Stem words which are synonymous with an action word.
    'adjust': 'edit',
    'alter': 'edit',
    'chang': 'edit',
    'modifi': 'edit',
    'begin': 'new',
    'creat': 'new',
    'start': 'new',
    'remov': 'delete',
    'destroy': 'delete',
    'dump': 'delete',
    'list': 'display',
    'show': 'display',
    'print': 'display',
    'ye': 'yes',
    'ya': 'yes',
    'yeah': 'yes',
    'sure': 'yes',
    'ok': 'yes',
    'okay': 'yes',
    'nope': 'no',
}
VARIABLES = {
    # Stored by function_name as key.
}


def _get_action_from_text(text: str, keyword: str):
    """Based upon the text input, determine which action to take."""
    filtered_text = []
    LOGGER.debug('Raw text to get action from: "{}".'.format(text))
    if text in ADMIN_ACTIONS:
        action = ADMIN_ACTIONS[text]
    else:
        for word in text.split():
            if word in SYNONYMS:
                filtered_text = [SYNONYMS[word]]
                break
            elif word in IGNORE_WORDS:
                continue
            else:
                filtered_text.append(word)
        text = ' '.join(filtered_text)
        LOGGER.debug('Filtered text: "{}".'.format(text))
        available = globals()
        funct_name = '_'.join([text, keyword])
        if funct_name in available:
            action = available[funct_name]
        else:
            action = None
    return action


def _get_yes_or_no(prompt='Please say "yes" or "no".') -> bool:
    """Prompt the user for a 'yes' or 'no' response."""
    response = listener.get_user_input(prompt, interpret=False)
    LOGGER.debug('Raw response: "{}".'.format(response))
    if response in SYNONYMS:
        response = SYNONYMS[response]
    LOGGER.debug('The parsed response was: "{}".'.format(response))
    return 'yes' in response


def _get_help(options: dict):
    """Display help for the current options."""
    opts = []
    for index, option in enumerate(sorted(list(options.keys()))):
        # Example: "1) Create a new function"
        opt = '{}) {}'.format(index + 1, option)
        _status_update(opt)
        opts.append(opt)
    return opts


def _run_menu(title: str, options: dict, **kwargs) -> list:
    """Run a menu with the given title and options."""
    LOGGER.debug('Starting the {} menu.'.format(title))
    _status_update('Welcome to the {} Menu.'.format(title))
    _status_update('Please make a selection from the following options:')
    _get_help(options)
    results = []
    while True:
        os.system('clear')  # Clear out any previous text.
        raw_choice = listener.get_user_input()

        # Get the help dialogue.
        if 'help' in raw_choice:
            _get_help(options)
            continue

        # Otherwise determine which action to take.
        # TODO: Support using the index number instead of name.
        action = _get_action_from_text(raw_choice, kwargs['keyword'])
        if not action:
            LOGGER.warning('User choice "{}" had no matches.'.format(raw_choice))
            _status_update('The choice you selected does not exist.')
            continue
        else:
            # Run the action:
            _status_update('Okay, doing that now.')
            result = action(**kwargs)
            results.append(result)
            # Determine if anything else is needed.
            if _get_yes_or_no('Do you want to do anything else?'):
                continue
            else:
                _status_update('Good bye.')
                break
    return results


def _status_update(text: str) -> None:
    """Provide a status_update in text and audio, which also logs locally."""
    listener.status_update(text)
    LOGGER.info(text)


def _var_exists(function_name: str, var_name: str) -> bool:
    """Validate that the requested function exists for the function."""
    if function_name not in VARIABLES or var_name not in VARIABLES[function_name]:
        msg = 'The requested function_name or variable is not defined.'
        LOGGER.warning(msg)
        _status_update(msg)
        exists = False
    else:
        exists = True
    return exists


def new_function(**kwargs):
    """Create a new function."""
    # TODO: Should this be within its own menu so we can continue/break?
    LOGGER.info('Creating a new function.')
    template = '''
    def {name}({input_vars}) -> {returns}:
        """{docstr}"""
        {logic}
    '''
    raw_name = listener.get_user_input('What would you like to name the function?')
    # TODO: How do we clean this up, yet not remove meaningful words?
    name = '_'.join(raw_name)
    _status_update('The function is now named "{}".'.format(name))
    # TODO: Reduce redundancy among new/edit/delete/display functions.
    description = listener.get_user_input('What would you like in the description?', interpret=False)
    _status_update('The function description is now: {}.'.format(description))
    input_vars = _run_menu('Function Input', {'Create a new variable': new_variable,
                                   'Edit a variable': edit_variable,
                                   'Delete a variable': delete_variable,
                                   'Display a variable': display_variable}, function_name=name, keyword='variable')
    _status_update('The input variables are now: {}'.format(', '.join(sorted([v[name] for v in input_vars]))))
    logic_lines = _run_menu('Logic', {'Create a new line': new_line,
                                'Edit a line': edit_line,
                                'Delete a line': delete_line,
                                'Display all lines': display_lines}, function_name=name, keyword='line')
    _status_update('Finished updating the logic lines.')
    if _get_yes_or_no('Should the function return anything?'):
        # TODO: Simplify this phrase... the user shouldn't need to know about yield/return.
        response = listener.get_user_input('Should this return or yield?')
        if 'yield' in response:
            output = 'yield {}'
        else:
            output = 'return {}'
        # TODO: Add support for returning/yielding multiple variables.
        msg = 'Which variable do you want to return?\nPlease choose from:\n{}'
        return_var = listener.get_user_input(msg.format('\n'.join(input_vars)))
        logic_lines.append(output.format(return_var))
    else:
        return_var = 'None'
    formatted = template.format(name=name, input_vars=input_vars, returns=return_var, docstr=description,
                                logic=logic_lines)
    # TODO: Do something safer than eval here.
    LOGGER.info('Interpreting the function source code.')
    LOGGER.debug('Source code:\n{}'.format(formatted))
    FUNCTIONS[name] = eval(formatted)
    return formatted


def new_line(function_name: str, **kwargs):
    """Add a new logic line to a function."""
    # TODO: We also need to recognize variable names which are defined within the function's scope.
    variables = VARIABLES[function_name]
    # TODO: How do we get advanced usage in here?
    line = listener.get_user_input('What do you want this line of code to do?', interpret=False)
    if function_name not in LOGIC_LINES:
        # TODO: defaultdict(list)?
        LOGIC_LINES[function_name] = []
    LOGIC_LINES[function_name].append(line)
    return line


def edit_line(function_name: str, **kwargs):
    """Edit a line of logic for a function."""
    pass


def delete_line(function_name: str, **kwargs):
    """Delete a line of logic from a function."""
    pass


def display_lines(function_name: str, **kwargs):
    """Display lines of logic from a function."""
    for index, line in enumerate(LOGIC_LINES[function_name]):
        # Example: '1) c = a + b
        _status_update('{}) {}'.format(index, line))


def new_variable(function_name: str, **kwargs):
    """Create a new variable."""
    raw_name = listener.get_user_input('What would you like to name the variable?')
    # TODO: How do we clean this up, yet not remove meaningful words?
    name = raw_name.replace(' ', '_')
    if name in VARIABLES[function_name]:
        if not _get_yes_or_no('The variable "{}" already exists.  Do you want to replace it?'.format(name)):
            variable = VARIABLES[function_name][name]
            return variable
    # TODO: Simplify the options here: i.e. empty, numerical, text, list, dictionary, other...
    # TODO: Simple choices with validation.
    var_type = listener.get_user_input('What type is this variable?')
    return {'name': name, 'type': var_type}


def edit_variable(function_name: str, **kwargs):
    """Edit a variable."""
    var_name = listener.get_user_input('Which variable do you want to edit?', interpret=False)
    LOGGER.debug('Editing variable "{}".'.format(var_name))
    if _var_exists(function_name, var_name):
        VARIABLES[function_name][var_name] = new_variable(function_name)
        msg = 'Successfully Updated "{}".'.format(var_name)
        _status_update(msg)
        LOGGER.info(msg)


def delete_variable(function_name: str, **kwargs):
    """Delete a variable."""
    var_name = listener.get_user_input('Which variable do you want to delete?', interpret=False)
    LOGGER.debug('Deleting variable "{}".'.format(var_name))
    if _var_exists(function_name, var_name):
        if _get_yes_or_no('Are you sure that you want to delete "{}"?'.format(var_name)):
            del VARIABLES[function_name][var_name]
            msg = 'Successfully Deleted "{}".'.format(var_name)
            _status_update(msg)
            LOGGER.info(msg)
        else:
            _status_update('Did not delete "{}".'.format(var_name))


def display_variable(function_name: str, **kwargs):
    """Display a variable."""
    var_name = listener.get_user_input('Which variable do you want to display?', interpret=False)
    LOGGER.debug('Displaying variable "{}".'.format(var_name))
    if _var_exists(function_name, var_name):
        var_cfg = VARIABLES[function_name][var_name]
        _status_update('Name: {}.  Type: {}.'.format(var_cfg['name'], var_cfg['type']))


def edit_function(**kwargs):
    """Edit an existing function."""
    funct_name = listener.get_user_input('Which function do you want to edit?', interpret=False)
    LOGGER.info('Editing function "{}".'.format(funct_name))
    pass


def delete_function(**kwargs):
    """Delete an existing function."""
    funct_name = listener.get_user_input('Which function do you want to delete?', interpret=False)
    LOGGER.info('Deleting function "{}".'.format(funct_name))
    if funct_name not in FUNCTIONS:
        _status_update('The function "{}" is not defined.'.format(funct_name))
    else:
        del FUNCTIONS[funct_name]


def display_function(**kwargs):
    """Display the current status of a function."""
    funct_name = listener.get_user_input('Which function do you want to display?', interpret=False)
    LOGGER.info('Displaying function "{}".'.format(funct_name))
    if funct_name not in FUNCTIONS:
        _status_update('The function "{}" is not defined.'.format(funct_name))
    else:
        _status_update(FUNCTIONS[funct_name])


def save_function(**kwargs):
    """Save the current code."""
    funct_name = listener.get_user_input('Which function do you want to save?', interpret=False)
    LOGGER.info('Saving function "{}".'.format(funct_name))
    pass


def main() -> None:
    """Main menu initiation."""
    LOGGER.info('Starting the main menu.')
    menu_opts = {
        'Create a new function': new_function,
        'Edit a function': edit_function,
        'Delete a function': delete_function,
        'Display a function': display_function,
        'Save a function': save_function,
    }
    _run_menu('Main', menu_opts, keyword='function')


if __name__ == '__main__':
    main()
