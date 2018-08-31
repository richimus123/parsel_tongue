# coding=utf-8
"""Simple Python editor tasks via easy menus."""

import textwrap

import menu


class FunctionInputMenu(menu.Menu):
    """A sub-menu for editing a function's input variables."""
    pass


class FunctionLogicMenu(menu.Menu):
    """A sub-menu for editing a function's logic."""
    pass


class FunctionMenu(menu.Menu):
    """A menu for editing/creating a function."""

    sub_menus = [FunctionInputMenu]
    template = textwrap.dedent('''
    def {name}({input_vars}:
        """{desc}"""
        {logic}
    ''')

    def __init__(self):
        choices = [
            'edit name',
            'edit description',
            'edit input',
            'edit logic',
            'finish editing',
        ]
        super(FunctionMenu, self).__init__('New Function', choices)
        self._funct_name = self.funct_name()
        self._funct_desc = self.funct_description()
        # TODO: Support kwargs-like input.
        # TODO: Add full-support for mixed args, kwargs, etc.
        self._funct_input = self.funct_input_variables()
        self._funct_logic = self.funct_logic()
        # TODO: Test-run a function?
        # TODO: Auto-write unit tests?
        self.run_menu()

    def funct_name(self) -> str:
        """Edit the function's name."""
        name = self.get_user_input('What would you like to name the function?', convert_spaces=True)
        return name

    def funct_description(self) -> str:
        """Edit the function's description/docstring."""
        desc = self.get_user_input('What would you like in the description?', interpret=False)
        return desc

    def funct_input_variables(self) -> list:
        """Edit the input variables for the function."""
        # TODO: Do a sub-menu here.
        return []

    def funct_logic(self) -> str:
        """Edit the logic within a function."""
        # TODO: Do a sub-menu here.
        return """pass"""

    def finish_editing(self) -> None:
        """Finish editing, save/write the function."""
        # TODO: Write out to a file?
        funct_text = self.template.format(name=self._funct_name,
                                          desc=self._funct_desc,
                                          input_vars=', '.join(self._funct_input),
                                          logic=self._funct_logic)
        menu.status_update(funct_text)
