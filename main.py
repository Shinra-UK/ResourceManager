#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Shinra-UK"
__version__ = "0.0.2"
__license__ = "N/A"

import logging

import discordintegration
import tests

logging.basicConfig(level=logging.INFO)


def main():
    """ Main entry point of the app """
    print("Hello World!")

    tests.character_tests()
    tests.settlement_tests()
    tests.task_tests()

    # discordintegration.discord_integration()
    print("Goodbye World!")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
