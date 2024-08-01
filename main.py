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
import shutil

# === DEBUG ===
from pprint import pprint


# === COLOUR CLI ===


# === ===

# Creates public list and public string
directory_list = []
file_set = set()
file_output = ""

# print(Fore.RED + "I AM RED")

# === CLASSES ===

"""
Manages directory, and file paths
:path: Path for dir
:srcDirDef: Default value for if this is a soruce directory
"""


class directory:
    def __init__(self, path="", masterDir=0, srcDirDef="n"):
        # You should actually use set and get methods for input and output validation, but nah. Too lazy :3
        self._no_more_scans = False
        try:

            self._path = path or self.validate_path(
                Prompt.ask(
                    f"Input directory to scan [blue]{escape("[or press 'enter' to continue]")}[/blue]"
                )
            )
            # if(not self._path):
            # break

            # If this is a directory to be scanned against
            self._source_dir = masterDir or self.validate_source_dir(
                Prompt.ask(
                    f"Scan against this directory [magenta]{escape("[y/n]")}[/magenta]? def:",
                    default=srcDirDef,
                )
            )
            self._list_of_files, self._list_of_dirs, self._list_of_unkowns = (
                self.explore_files(self._path)
            )

        # except SpecialException:
        #    raise ValueError("SPECIAL I AM 02")
        except ValueError:
            print(ValueError, "[yellow] Catch me ")
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
        # try:
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
            # print(path_input, " has been added")
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
        print("Output path does not exist: [dark_orange]" + path.realpath(path_input))
        create_dir = Confirm.ask(
            "[yellow] Provided path does not exist, want to create one?",
            choices=["y", "n"],
        )
        if create_dir == "y":
            return path_input
        else:
            return validate_output_path(input("Provide a path for file output: "))

        # Todo: if create_dir == true ==>  mkdir / create dir else ask for input
    # print("[dark_orange] Will implement later to create dir")

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
    # for master_directory in directory_list:
    #     if master_directory._source_dir == True:
    #         for scan_directory in directory_list:
    #             if master_directory != scan_directory:
    # # TODO: Scann each file w/o ext against all other and add its path to a 'set' as 'set's  dosen't tolerate duplicates

    # '''
    # for each master_file in master_dir:
    #     for each scan_file in scan_dir:
    #         if master_file_no_ext == scan_file_no_ext
    #             add filepath for both to file_list_set
    # '''

    # '''
    # :master_dir:
    # :compare_dir:

    # foreach master_dir -> put file names in a set

    # then
    # compare compare_dir.name aginst set. If match  -> 3rd_prt_set

    # loop master_dir -> map(name, path)
    #     put in set

    # loop compare_dor -> map(name, path) against set
    #     if true
    #         set to dir.

    # '''
    source_dir = set()

    for _directory in directory_list:
        if _directory._source_dir == True:
            for file_obj in _directory._list_of_files:
                source_dir.add(path.splitext(file_obj.name)[0])
                # ? Assumes that if a file is in source_directory, it is regarldes of a pair added to file_set
                file_set.add(file_obj.path)

    for _file in source_dir:
        print(_file)
        # print(dir(_file))
        # print(path.splitext(_file.name)[0])
        # print(path.splitext(_file.name)[1])
        # print((_file.path))
        # break

    for _directory in directory_list:
        if _directory._source_dir == False:
            for file_obj in _directory._list_of_files:

                if path.splitext(file_obj.name)[0] in source_dir:
                    file_set.add(file_obj.path)

    for _file in file_set:
        print(_file)


def move_files(file_paths, file_output):
    # Todo: Move all files from file_set to file_output
    # Todo: If file_output does not exist, create dir
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
                    "[Red] 89 error WARNING FILE OVERWRITE CALNCELS ",
                )
            # except (NotADirectoryError, OSError) as err:
            except Exception as err:

                print(
                    Exception,
                    OSError,
                    "[red] WARNING: POTENTIAL DUPPLICATE FILE NAME",
                    err,
                )
                print(file_source)
                print("Name of file: ", path.split(file_source))
                print("[yellow]DEB:: Split: ", path.split(file_source))
                print("[yellow]DEB:: splitext: ", path.splitext(file_source))
                print("[yellow]DEB:: basename: ", path.basename(file_source))
                print(
                    "[yellow]DEB:: splittext(basename): ",
                    path.splitext(path.basename(file_source)),
                )
                # ! IF Exception arises. IT IS HERE you prompt for filename-change and moves the file, then it goes back to the loop
                # ? If you sugest duplicate filename "file.txt" --> "file-1.txt", maybe check file_set for "file-1.txt" just in case, ...
                # ? ... and of course ask user of thier opinion
                # TODO: S: If exception. Fix dupplicate file, ask user or something. The go back and continue to move files
                # Todo: M: Loop exits when exception is casted. Continue loop
                # Todo: M: Dupplicate file HAS NOT BEEN MOVED
                print("")
                print(file_source)
                temp_path = path.split(file_source)[0]  # aka. dirname
                temp_file = path.split(file_source)[1]  # aka. basename
                temp_file_name = path.splitext(temp_file)[0]
                temp_file_ext = path.splitext(temp_file)[1]
                # Todo: C: Show file info, like timestamps, size etc...
                print(temp_path, temp_file, temp_file_name, temp_file_ext)

                count = 1
                while True:
                    temp_file_name_new = temp_file_name + "-" + str(count)
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
                    # print(
                    #     "[yellow]DEB:: // New:"
                    #     + path.join(temp_path, temp_file_name_new + temp_file_ext)
                    # )
                    # print("[yellow]DEB:: Old:" + file_source)
                    # print("[yellow]DEB:: Out:" + file_output)
                    # print("[yellow]DEB:: New Out:" + _temp_file_output)
                    #! shutil throws: "[WinError 3] The system cannot find the path specified"
                    print("")
                    print("[yellow]DEB:: Filesource: [yellow2]", file_source)
                    print("[yellow]DEB:: New file output: [yellow2]", _temp_file_output)
                    print(
                        "[yellow]DEB:: Is file_soruce a file?: [yellow2]",
                        os.path.isfile(file_source),
                    )
                    print("[yellow]DEB:: New file output: [yellow2]", _temp_file_output)
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
                    os.remove(file_output)
                    shutil.move(file_source, file_output)
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
        print("[Red] 89 error WARNING FILE OVERWRITE CALNCELS ")
    except (NotADirectoryError, OSError) as err:

        print(Exception, "[red] WARNING: POTENTIAL OVERWRTIRES, CANCELS PROCESS", err)
        # TODO: If exception. Fix dupplicate file, ask user or something. The go back and continue to move files

    except OSError:
        pass


# ===== RUNNING =====


# _dir = ""
# Iterates and gets all dirs to be scanned

_dir = directory("", 0, "y")
if _dir._no_more_scans is False:
    directory_list.append(_dir)
print(_dir._path)
print(_dir._source_dir)
print(_dir._list_of_files)

while True:
    # // Todo: Take inputs
    # // Todo: Add inputs to list
    # Todo: Check that there are at least one dir to scan against and at least one dir to scan for
    # Todo: Could be done with simple global booleans
    # Todo: Add a duplicate path filter

    _dir = directory()

    #! -- DEBUG --
    # print(type(_dir))
    # print(dir(_dir))
    if _dir._no_more_scans is False:
        print("[yellow] DEB:: Printing all files")
        for _path in _dir._list_of_files:
            print("[cyan] " + _path.path)
        # print(_path.stat().st_type)
        print("")

    if _dir._no_more_scans is False:
        directory_list.append(_dir)
    else:
        break

file_output = validate_output_path(input("Path for file output: "))

print("[yellow]DEB:: Got out of the loop")

search_directories_for_similar_files(directory_list)

move_files(file_set, file_output)

input("Press ENTER to exit the program...")


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


# DEFAULT FOR SCAN AGIANST IN PROMPT CLI --> (n)
