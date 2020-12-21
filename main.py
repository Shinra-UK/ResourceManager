#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Shinra-UK"
__version__ = "0.0.1"
__license__ = "N/A"

import characters
import discordintegration
import logging


logging.basicConfig(level=logging.INFO)


def main():
    """ Main entry point of the app """
    print("Hello World!")
    test_mc_gee = characters.createCharacter("Test Mcgee")
    test_mo_jo = characters.createCharacter("Test Mo Jo")
    print(test_mc_gee)
    print(test_mo_jo)
    print(characters.Character.character_list)
    discordintegration.discord_integration(characters.Character.character_list)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
