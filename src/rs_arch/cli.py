"""
Module containing main CLI entry point.
"""

from typing import Callable

import questionary


def cli() -> int:
    """Main CLI entrypoint."""
    choice_callback = main_menu_selection()
    choice_callback()
    return 0


def main_menu_selection() -> Callable[[], None]:
    """Print the main menu and get a selection."""
    choice_map = {
        'Update current material storage': lambda: None,
        'Update artefacts to track': lambda: None,
        'Get materials needed for artefacts': lambda: None,
        'Print current material storage': lambda: None,
        'Print artefacts being tracked': lambda: None,
        'Clear material storage': lambda: None,
        'Clear artefacts being tracked': lambda: None,
        'Exit': lambda: None,
    }

    question = questionary.select(
        'Main Menu',
        choices=[
            'Update current material storage',
            'Update artefacts to track',
            'Get materials needed for artefacts',
            'Print current material storage',
            'Print artefacts being tracked',
            'Clear material storage',
            'Clear artefacts being tracked',
            'Exit',
        ],
        use_shortcuts=True,
    )
    return choice_map[question.ask()]


if __name__ == '__main__':
    raise SystemExit(cli())
