# coding=utf-8
"""Helpers for working with functions."""

import lib
import var_lib

TEMPLATE = '''
def {name}({input_vars}):
    """{description}"""
{logic_lines}
    '''


def create_function():
    """Create a new function."""
    name = lib.simple_prompt('What do you want to name the function?')
    desc = lib.simple_prompt('What do you want in the description?')
    if lib.get_yes_or_no('Does the function require input variables?'):
        input_vars = var_lib.create_variables(as_input_vars=True)
    else:
        input_vars = {}
    parsed_vars = ', '.join(input_vars.values())
    lib.status_update('Great.  Now let\'s add some logic lines.')
    logic_lines = lib.create_logic_lines()
    funct = TEMPLATE.format(name=name, input_vars=parsed_vars, description=desc, logic_lines=logic_lines)
    return funct


@lib.not_implemented
def delete_function(funct):
    """Delete an existing function."""
    options = {}
    # TODO: How do we return things properly from the menu?  Yield?
    lib.run_menu('Delete a Function', options, display=funct)
    return funct


@lib.not_implemented
def edit_function(funct):
    """Edit an existing function."""
    options = {}
    # TODO: How do we return things properly from the menu?  Yield?
    lib.run_menu('Edit a Function', options, display=funct)
    return funct
