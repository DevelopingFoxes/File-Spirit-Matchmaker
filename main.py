# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:47:04 2024

@author: Paw
"""

# COPY PASTA

# C:\Users\_\Documents\temp\1
# C:\Users\_\Documents\temp\1\1.txt
# C:\Users\_\Documents\temp\2\1.png

# * ===== THE LIST ===== *

# // Todo: Take inputs
    # // Todo: Add inputs to list
    # Todo: Check that there are at least one dir to scan against and at least one dir to scan for
    # Todo: ^^ Could be done with simple global booleans
    # // Todo: Add a duplicate path filter
    # Todo: S: Option wherter to copy or move files etc.
    # Todo: C: Seperate files into different sub cateogies based on extentions (could flags certain ext.)
    # Todo: S: Colour schema does not work well in black terminals (eg. CMD), fix a colourschema variables for easier change and management
    # Todo: S: See 'todo' in funciton move_files()
    # Duplicate files options: yes to all

# === IMPORTS ===

from pathlib import Path
import os
from os import path
from os.path import join, getsize
from rich import print
from rich.prompt import Prompt, Confirm
from rich.markup import escape
import shutil

# === DEBUG ===
from pprint import pprint

# === PUBLIC VARS ===

# Creates public list and public string
directory_list = []
file_set = set()
file_output = ""


# === CLASSES ===

"""
Manages directory, and file paths
:path: Path for dir
:srcDirDef: Default value for if this is a soruce directory
"""
class directory:
    def __init__(self, path="", masterDir=0, srcDirDefault="n"):
        # You should actually use set and get methods for input and output validation, but nah. Too lazy :3
        self._no_more_scans = False
        try:

            self._path = path or self.validate_path(
                Prompt.ask(
                    f"Input directory to scan [blue]{escape("[or press 'enter' to continue]")}[/blue]"
                )
            )

            # If this is a directory to be scanned against
            self._source_dir = masterDir or self.validate_source_dir(
                Prompt.ask(
                    f"Scan against this directory [magenta]{escape("[y/n]")}[/magenta]? def:",
                    default=srcDirDefault,
                )
            )
            self._list_of_files, self._list_of_dirs, self._list_of_unkowns = (
                self.explore_files(self._path)
            )

        except ValueError:
            # Uses ValueError to break out of loop
            self._no_more_scans = True

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
        # Filepath is empty, break
        if not path_input:
            raise ValueError("SPECIAL I AM 02")
            return False
        # Checks if filepath exists
        if not path.exists(path_input):
            print("[dark_orange] Path does not exist")
            path_input = input("Correct the path and input the path again: ")
            return self.validate_path(path_input)
            ## todo: loop back for new statement or ask to got to the parrent

        # Checks if dirPath is a dir
        if path.isdir(path_input):
            return path_input

            print(path_input, " has been added")

        elif path.isfile(path_input):
            # If dirPath is a file, assumes the same directory

            print("[grey35]Converted path: '" + path_input + "'")
            path_input = path.dirname(path_input)
            print("[grey35]Into path directory: [white]" + path_input)
            return path_input
        else:
            print("[red] Could not handle path, validate path and try again")

    def validate_source_dir(self, value_input):
        try:
            if value_input == "":
                print("[yellow] Blank is assumes as 'no'")
                val = Prompt.ask(
                    f"[blue] Confirm with 'enter' for [cyan]'n'[/cyan] or type {escape("[y/n]")}..."
                )
                if val == "":
                    return False
                else:
                    return self.validate_source_dir(val)

            for val in ["n", 0, "no"]:
                if value_input == val:
                    print(
                        "Will not scan against provided directory: [cyan]" + value_input
                    )
                    return False
            for val in ["y", 1, "yes"]:
                if value_input == val:
                    print("Will scan against provided directory: [cyan]" + value_input)
                    return True
            else:
                raise ValueError("[yellow] Invalid input, write 'y' or 'n'")
        except ValueError:
            val = input(
                f"[yellow] Invalid input, Scan against this directory {escape("[y/n]")}? "
            )
            val = self.validate_source_dir(val)
            return val


# ===== FUNCTIONS =====


def validate_output_path(path_input):
    # Filepath is empty, break
    if not path_input:
        print("[dark_orange] Path for output is empty, provide a path for output")
        path_input = input("Output path: ")
        return validate_output_path(path_input)

    # Checks if filepath exists
    if not path.exists(path_input):
        print(
            "[dark_orange]Output path does not exist: [orange4]"
            + path.realpath(path_input)
        )
        create_dir = Confirm.ask(
            "[yellow] Provided path does not exist, want to create one?",
            choices=["y", "n"],
        )
        if create_dir:
            try:
                os.makedirs(path_input)
                if path.isdir(path_input):
                    print("[yellow]Filepath has been created: ", path_input)
                else: 
                    print("[red]Something whent wront :(")                    
            except Exception as err:
                print(err)
                raise Exception
            return path_input
        else:
            return validate_output_path(input("Provide a path for file output: "))

    # Checks if dirPath is a dir
    if path.isdir(path_input):
        print("Will output to: ", path_input)
        return path_input

    elif path.isfile(path_input):
        # If dirPath is a file, assumes the same directory
        output_dir = Confirm.ask(
            "[dark_orange] Path for output is to a file, want to output to same direcrory as the file?",
            choices=["y", "n"],
        )
        if output_dir == "y":
            path_input = path.dirname(path_input)
            print("Converted path to: '", path_input, "'")
        else:
            return validate_output_path(input("Provide a path for file output: "))

        return path_input
    else:
        print("[red] Could not handle path, validate path and try again")



# ===== Functions =====


def add_path_to_directory_list(dir_path):
    directory_list.append(dir_path)


"""
:param directory_list: takes a array of filepaths:str
"""


def search_directories_for_similar_files(directory_list):
    
    source_dir = set()

    for _directory in directory_list:
        if _directory._source_dir == True:
            for file_obj in _directory._list_of_files:
                source_dir.add(path.splitext(file_obj.name)[0])
                # ? Assumes that if a file is in source_directory, it is regarldes of a pair added to file_set
                file_set.add(file_obj.path)

    for _directory in directory_list:
        if _directory._source_dir == False:
            for file_obj in _directory._list_of_files:

                if path.splitext(file_obj.name)[0] in source_dir:
                    file_set.add(file_obj.path)

def move_files(file_paths, file_output):
    try:
        for file_source in file_set:
            try:
                shutil.move(file_source, file_output)
                print("[orange4]Moved file from: " + file_source)

            except FileExistsError as err:
                print(FileExistsError, err)
                for _err in FileExistsError:
                    print(_err)
                print(
                    FileExistsError,
                    err,
                
                )
            except Exception as err:

                # print(
                #     Exception,
                #     OSError,
                #     "[orange] WARNING: POTENTIAL DUPPLICATE FILE NAME",
                #     err,
                # )
                
                temp_path = path.split(file_source)[0]  # aka. dirname
                temp_file = path.split(file_source)[1]  # aka. basename
                temp_file_name = path.splitext(temp_file)[0]
                temp_file_ext = path.splitext(temp_file)[1]
                # Todo: C: Show user the file info, like: timestamps, size etc...

                # Checks for duplicate files names before sugesting a unique file name
                count = 1
                while True:
                    temp_file_name_new = temp_file_name + "_" + str(count)
                    if not temp_file_name_new in file_set:
                        break
                    else:
                        count += 1
                print(
                    f"[red]Duplicate file name found: [white]{temp_file_name} ({temp_file_ext})"
                )
                temp_prompt = Prompt.ask(
                    f"What action to do?[cyan] Default rename to: [cyan]{temp_file_name_new + "(" +temp_file_ext})? [blue]{escape("[ENTER]")}[/blue]:",
                    choices=["Yes", "Skip", "Replace", "Custom Name"],
                    default="Yes",
                )

                if temp_prompt == "Yes" or "yes" or "y" or 1:
                    _temp_file_output = path.join(
                        file_output, temp_file_name_new + temp_file_ext
                    )
                    
                    shutil.move(
                        file_source,
                        _temp_file_output,
                    )
                    print(
                        "[orange4] File was moved: "
                        + path.join(temp_path, temp_file_name_new + temp_file_ext)
                    )
                elif temp_prompt == "Skip" or "skip" or "s":
                    print(f"[orange4] File {file_source} was skipped")
                elif temp_prompt == "Replace" or "replace" or "r":
                    _prmp = Prompt.ask("[red]You are sure you want to REPLACE the file", choices=['n','y'],default='y')
                    if(_prmp == "y"):
                        os.remove(file_output)
                        shutil.move(file_source, file_output)
                    else:
                        raise Exception
                        # Todo: S: Make function move_files call a "move_file" funciton so it can be called from other sources

                    print(f"[orange4] File {file_source} was replaced")

                elif temp_prompt == ("Custom Name" or "custom name" or "c" or "cn"):
                    temp_file_name_new = Prompt.ask(
                        "Select new file name (without extention): "
                    )
                    shutil.move(
                        path.join(temp_path, temp_file_name_new + temp_file_ext),
                        file_output,
                    )
                    print(
                        "[orange4] File was moved: "
                        + path.join(temp_path, temp_file_name_new + temp_file_ext)
                    )

    except FileExistsError as err:
        print(FileExistsError, err)
        for _err in FileExistsError:
            print(_err)
        print("[Red] ERROR")
    except (NotADirectoryError, OSError) as err:

        print(Exception, "[red] ERROR", err)

    except OSError:
        pass


# ===== RUNNING =====


# _dir = ""
# Iterates and gets all dirs to be scanned

_dir = directory("", 0, "y")
if _dir._no_more_scans is False:
    directory_list.append(_dir)

while True:
    
    _dir = directory()    

    if _dir._no_more_scans is False:
        directory_list.append(_dir)
    else:
        break

file_output = validate_output_path(input("Path for file output: "))

search_directories_for_similar_files(directory_list)

move_files(file_set, file_output)

input("Press ENTER to exit the program...")


