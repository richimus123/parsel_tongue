# coding=utf-8
"""Helpers for working with classes."""

import lib

# TODO: Auto-add built-ins like __str__, __repr__, etc.
CLASS = '''
class {name}({parent}:
    """{desc}"""
    {class_attrs}

    def __init__(self, {inst_attrs}):
        """{attrs_desc}"""
        {attrs}

    def __str__():
        """String respesentation of the class."""
        return self.__class__.__name__

'''
METHOD = '''
    def {name}(self, {input_vars}):
        """{desc}"""
        {logic_lines}
'''
PROPERTY = '''
    @property
    def {name}(self, {input_vars}):
        """{desc}"""
        {logic_lines} 
'''


@lib.not_implemented
def create_class():
    """Create a new class."""
    pass


@lib.not_implemented
def delete_class():
    """Delete a class."""
    pass


@lib.not_implemented
def edit_class():
    """Edit a class."""
    pass
