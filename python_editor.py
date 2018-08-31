# coding=utf-8
"""Simple Python editor tasks via easy menus."""

import textwrap

import menu

# TODO: Add logging, asyncio for performance gains.
# TODO: Needs unit tests/performance benchmarks, etc.


class FunctionInputMenu(menu.Menu):
    """A sub-menu for editing a function's input variables."""
    # TODO: Add full-support for mixed args, kwargs, etc.
    pass


class FunctionLogicMenu(menu.Menu):
    """A sub-menu for editing a function's logic."""
    # TODO: Intuitive editing commands:
    # new line
    # make a variable
    # return
    # yield
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
            'edit function name',
            'edit function description',
            'edit function input',
            'edit logic',
            'save',
        ]
        super(FunctionMenu, self).__init__('New Function', choices)
        self._funct_name = 'no_name'
        self._funct_desc = ''
        self._funct_input = []
        self._funct_logic = 'pass'
        self._funct_text = ''
        # TODO: Test-run a function?  eval/literal_eval it and then run it?
        # TODO: Auto-write unit tests?
        self.run_menu(ignore_words=('edit', ))

    def function_name(self) -> None:
        """Edit the function's name."""
        name = self.get_user_input('What would you like to name the function?', convert_spaces=True)
        self._funct_name = name

    def function_descript(self) -> None:
        """Edit the function's description/docstring."""
        desc = self.get_user_input('What would you like in the description?', interpret=False)
        self._funct_desc = desc

    def function_input(self) -> None:
        """Edit the input variables for the function."""
        # TODO: Do a sub-menu here.
        input_vars = self.get_user_input('What would you like to name the input variables?', interpret=False)
        self._funct_input = input_vars.split()

    def function_logic(self) -> None:
        """Edit the logic within a function."""
        # TODO: Do a sub-menu here.
        logic = self.get_user_input('What would you like the function to do?', interpret=False)
        self._funct_logic = logic

    def save(self) -> None:
        """Finish editing, save/write the function."""
        # TODO: Write out to a file?
        funct_text = self.template.format(name=self._funct_name,
                                          desc=self._funct_desc,
                                          input_vars=', '.join(self._funct_input),
                                          logic=self._funct_logic)
        self._funct_text = funct_text
        menu.listener.status_update(funct_text)
