# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:47:04 2024

@author: Paw
"""

## TODO

## CLI INTERFACE

## Input: <Foler path to Scan Dir>
### DOCS: Scan folder (non recursive) and make a multi-dimentional list [file_no_extetion, file_with_extention, file path]

## Input: <Folder Path to Scan Dir>
### DOCS: Scan folder (non recursive) and make a --//--

### Input: <Folder Path to Output results>
"""
Save path for later.
Later: Move all files with matching names regardless of file extention. 
If mulitple files have the same full-file-name, add a count to the newer file, --> file.file, file-1.file

If folder does not exist, create folder
"""


## Input: <confirm OR add folder path>
"""
Display current config, confirm to proceed or to add another folder input.

"""
#
# COPY PASTA

# C:\Users\_\Documents\temp\1
# C:\Users\_\Documents\temp\1\1.txt
# C:\Users\_\Documents\temp\2\1.png


# === IMPORTS ===

from pathlib import Path
import os
from os import path
from os.path import join, getsize
from rich import print
from rich.prompt import Prompt, Confirm
from rich.markup import escape

# === DEBUG ===
from pprint import pprint


# === COLOUR CLI ===


# === ===

# Creates public list and public string
directory_list = []
files_list = []
fileoutput = ""

# print(Fore.RED + "I AM RED")

# === CLASSES ===


class directory:
    def __init__(self, path="", masterDir=0):
        self._no_more_scans = False
        try:

            self._path = path or self.validate_path(input("Input directory to scan: "))
            # if(not self._path):
            # break
            self._masterDir = masterDir or self.validate_masterDir(
                Prompt.ask(f"Scan against this directory [magenta]{escape("[y/n]")}?")
            )
            self._list_of_files, self._list_of_dirs, self._list_of_unkowns = (
                self.explore_files(self._path)
            )

        # except SpecialException:
        #    raise ValueError("SPECIAL I AM 02")
        except ValueError:
            print(ValueError, "[yellow] Catch me ")
            self.explore_files_no_more_scans = True

    """
    Non recursive scandir of direcrory path 
    Appends onlt files and not dirs to directory._list_of_files
    """

    def explore_files(self, path):
        # Todo: if slow, do this in an async method / thread
        scanned_dir = os.scandir(path)
        file_list = []
        dir_list = []
        unkown_list = []
        for path in scanned_dir:
            if os.path.isfile(path):
                file_list.append(path)
            elif os.path.isdir(path):
                dir_list.append(path)
            else:
                unkown_list.append(path)
                print("[yellow] Unkown path entry: ", path)

        return file_list, dir_list, unkown_list

    def validate_path(self, path_input):
        # try:
        # Filepath is empty, break
        if not path_input:
            raise ValueError("SPECIAL I AM 02")
            return False
        # Checks if filepath exists
        if not path.exists(path_input):
            print("[dark_orange] Filepath does not exist")
            raise ValueError("Path does not exist: ", path_input)
            ## todo: loop back for new statement or ask to got to the parrent

        # Checks if dirPath is a dir
        if path.isdir(path_input):
            return path_input

            print(path_input, " has been added")

        elif path.isfile(path_input):
            # If dirPath is a file, assumes the same directory

            print("Converted path: '", path_input, "'")
            path_input = path.dirname(path_input)
            print("Into path directory:", path_input)
            print(path_input, " has been added")
            return path_input
        else:
            print("[red] Could not handle path, validate path and try again")

    # except ValueError as error:
    #     for item in error:
    #         print(item)

    #     for item in ValueError:
    #         print(item)
    #     # print("[Yellow] deb error:: ", dir(error), error.args, dir(ValueError))
    #     # print("SPECIAL NOT I AM 01")

    #     raise ValueError("[red] Cannot handle file, unkown")

    def validate_masterDir(self, value_input):
        try:
            if value_input == "":
                print("[yellow] Blank is assumes as 'no'")
                val = Prompt.ask(
                    f"[blue] Confirm with 'enter' for [cyan]'n'[/cyan] or type {escape("[y/n]")}..."
                )
                if val == "":
                    return False
                else:
                    return self.validate_masterDir(val)

            for val in ["n", 0, "no"]:
                if value_input == val:
                    return False
            for val in ["y", 1, "yes"]:
                if value_input == val:
                    return True
            else:
                raise ValueError("[yellow] Invalid input, write 'y' or 'n'")
        except ValueError:
            val = input(
                f"[yellow] Invalid input, Scan against this directory {escape("[y/n]")}? "
            )
            val = self.validate_masterDir(val)
            return val


# def __repr__(self):
#    return self.list_of_files;


path_input = r"C:\Users\_\Documents\temp\1\1.txt"
print("===== OS PATH =====")
print("deb: Input path: ", path_input)
print("deb: ANY Exist: ", path.exists(path_input))
print("deb: Is-dir: ", path.isdir(path_input))
print("deb: Is_file: ", path.isfile(path_input))
print("deb: dirname: ", path.dirname(path_input))
print("")

"""
for root, dirs, files, dirfd in os.fwalk(
    print(root)
    print(dirs)
    print(files)
    print(dirfd)
    print("")
"""
print(os.scandir(path.dirname(path_input)))

with os.scandir(path.dirname(path_input)) as it:
    for entry in it:
        if not entry.name.startswith(".") and entry.is_file():
            print(entry.name)

print("")
print("")


# ===== Functions =====


def add_path_to_directory_list(dir_path):
    directory_list.append(dir_path)


"""
:param directory_list: takes a array of filepaths:str
"""


def search_directories_for_similar_files(directory_list):
    """
    TODO: If scan_against_this_dir is true
            Scan all other dirs agains this direcroty
            IF file is eq to file (w/o ext.) and file is not already in list
                Add thier dirEntry or just filepath to output
            Repeat for all dirs that are to be scanned against.


    """

    # for _dir in directory_list:
    #     pprint((_dir))
    #     for filepath in _dir.list_of_files:
    #         print((filepath))
    #     #     print((filepath.path))
    #     #     print((filepath.name))
    #     #     print((filepath.inode()))
    #     #     print(dir(filepath.stat()))
    #     #     print((path.splitext(filepath.name)[1]))
    # todo: where split(filepath)[1] against osther dirs is true; copy


# ===== RUNNING =====

_dir = ""
while True:
    # Todo: Take inputs
    # Todo: Add inputs to list

    _dir = directory()

    #! -- DEBUG --
    # print(type(_dir))
    # print(dir(_dir))
    if _dir._no_more_scans is False:
        for _path in _dir._list_of_files:
            print("[cyan] " + _path.path)
        # print(_path.stat().st_type)

    if _dir is False:
        directory_list.append(_dir)
    else:
        break

print("[yellow] Got out of the loop")


# Todo: Scan input list against one another
# Todo: If true, put all of those in thier own place
# Todo: Move all that is true


# path_input = {}
# path_input["path"] = input("Input directory to scan: ")
# path_input["masterDir"] = input("Scan against this directory? [y/n]") or 1
# print(path_input["masterDir"])
# for val in ["y", "n", 0, 1]:
#     if path_input["masterDir"] == val:
#         print("broken")
#         break
#     else:
#         print("not broken")


# # ! DEBUG
# if not path_input:
#     print("[yellow] path_input set to: " + r"C:\Users\_\Documents\temp\1\1.txt" + "\n")
#     path_input = r"C:\Users\_\Documents\temp\1\.txt"

# valid_path = validate_path(path_input)

# if valid_path:
#     add_path_to_directory_list(valid_path)
#     print("path added", valid_path)
# else:
#     # raise ValueError("Cannot handle file, unkown")
#     pass


# # DEB
# print("deb: directory_list:", directory_list)

# # ! PUT ME BACK
# # input("Input next directory to scan: ")
# path_input = r"C:\Users\_\Documents\temp\2\2.png"
# validated_path = validate_path(path_input)
# if validated_path:
#     add_path_to_directory_list(validated_path)
# else:
#     raise ValueError("Cannot handle file, unkown")


# print("deb: directory_list:", directory_list)

# print("")
# file_output = search_directories_for_similar_files(directory_list)
