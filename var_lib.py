# coding=utf-8
"""Helpers for working with variables."""

import lib

TEMPLATE = '''{name} = {value}  # type: {type}'''


def create_variables(as_input_vars=False) -> dict:
    """Create multiple variables interactively."""
    variables = {}
    while True:
        print('\nVariables:')
        for new_var in variables.values():
            print(new_var)
        variable, name = create_variable()
        if as_input_vars:
            # 'name = value  # type: type' -> 'name=value'
            name, value = variable.split(' = ')
            variable = '='.join([name, value.split()[0]])
        variables[name] = variable
        if not lib.get_yes_or_no('Do you want to create another variable?'):
            break
    return variables


def create_variable():
    """Create a new variable."""
    name = lib.simple_prompt('What do you want to name the variable?')
    value = lib.simple_prompt('What do you want as the initial value?')
    choices = {
        'none': {'action': lambda v: None, 'keyword': 'none', 'type': None},
        'number': {'action': lambda v: int(v), 'keyword': 'number', 'type': int},
        'decimal': {'action': lambda v: float(v), 'keyword': 'decimal', 'type': float},
        'text': {'action': lambda v: '"{}"'.format(str(v)), 'keyword': 'text', 'type': str},
        'list': {'action': lambda v: v.split(), 'keyword': ['list', 'array', 'multiple'], 'type': list},
        'dictionary': {'action': lambda v: dict(eval(v)), 'keyword': ['dict', 'dictionary'], 'type': dict},
    }
    var_type = lib.get_choice('What type should this variable be?', choices=choices)
    try:
        value = choices[var_type]['action'](value)
    except (TypeError, ValueError):
        lib.status_update('Failed to cast "{}" to a "{}".'.format(value, var_type))
    # Now set this to a structure like: 'name = value  # type: type'
    variable = TEMPLATE.format(name=name, value=value, type=choices[var_type]['type'])
    return variable, name


@lib.not_implemented
def delete_variable(funct):
    """Delete an existing variable."""
    options = {}
    # TODO: How do we return things properly from the menu?  Yield?
    lib.run_menu('Delete a Function', options, display=funct)


@lib.not_implemented
def edit_variable(funct):
    """Edit an existing variable."""
    options = {}
    # TODO: How do we return things properly from the menu?  Yield?
    lib.run_menu('Edit a Function', options, display=funct)
