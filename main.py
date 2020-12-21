#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Shinra-UK"
__version__ = "0.0.1"
__license__ = "N/A"

import characters
import discordintegration

def main():
    """ Main entry point of the app """
    print("Hello World!")
    characters.createCharacter()
    discordintegration.discord()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()