#!/usr/bin/python3

import argparse
import logging

import file_management

logging.basicConfig()
# logging,getLogger(None)

parser = argparse.ArgumentParser(description="Music manager for easy renaming, tagging, and organizing your music files.")
parser.add_argument("path", help="Path to the folder containing the music files")


USAGE = """
Usage: python3 main.py [options] [path]

Options:
"""

MENU = """
============================[ Music Manager ]============================
1. Rename files
2. Sanitize file names
2. Tag files        [x]
3. Organize files   [x]
4. Import files     [x]
5. Exit
==========================================================================

"""

# todo: create a check for a valid folder structure on the given path (from .env)
# todo: create a setup script that creates a folder structure and a .env file

def menu_loop():
    '''Main menu loop'''
    choice: int | None = None

    while True:
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                rename_files()
                break
            case 2:
                sanitize_files()
                break
            case 3:
                tag_files()
                break
            case 4:
                organize_files()
                break
            case 5:
                import_files()
                break
            case 6:
                print("Exiting...")
                exit(0)
            case _:
                print("Invalid choice, please try again.")
                break



if __name__ == "__main__":
    print("Music manager for easy renaming, tagging, and organizing your music files.\n\n")
    print("Created by @raoulkalkman\n")

    print(MENU)
    menu_loop()

