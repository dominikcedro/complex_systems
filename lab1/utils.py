"""
author: Dominik Cedro
date: 15.10.2024
description: Utility functions for better experience for the user
"""
import os

DIR_TO_CLEAR = './csv_output'

def remove_files_in_folder(dit_to_clear):
    # loop through all the contents of folder
    for filename in os.listdir(dit_to_clear):
        # remove the file
        os.remove(f"{dit_to_clear}/{filename}")


if __name__ == "__main__":
    remove_files_in_folder(DIR_TO_CLEAR)