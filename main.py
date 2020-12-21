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
    test_mc_gee = characters.create_character("Test Mcgee")
    test_mo_jo = characters.create_character("Test Mo Jo")
    test_mo_jo.ammend("gp", 20)
    test_mo_jo.ammend("gp", 200)
    test_mo_jo.ammend("gp", -640)
    test_mo_jo.ammend("gp", -40)
    test_mo_jo.ammend("name", 540)
    print(test_mo_jo.character_list)
    print(test_mc_gee.character_list)
    #discordintegration.discord_integration(characters.Character.character_list)
    print("Goodbye World!")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
