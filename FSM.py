# === IMPORTS ===

# CLI Arguments Handler
import argparse

# For argparse's type of path
import pathlib



# === CLI PARSER ===

def command_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # Source Arguments
    # Positional optional arguments
    source_args = parser.add_argument_group(
        "Source",
        description="Source directory argument. \nOne or multiple directories as a basis to compare files from",
    )
    source_args.add_argument(
        "source",
        nargs="?",
        type=pathlib.Path,
        help="Positional single source directory",
    )
    source_args.add_argument(
        "-s",
        "--source",
        action="extend",
        nargs="+",
        type=pathlib.Path,
        help="List of source directories",
    )

    # Search Arguments
    search_args = parser.add_argument_group(
        "Search",
        description="Search directory argument. \nOne or multiple directories to compare files against",
    )
    search_args.add_argument(
        "search",
        nargs="*",
        type=pathlib.Path,
        help="Positional single search directory",
    )
    search_args.add_argument(
        "-S",
        "--search",
        action="extend",
        nargs="+",
        type=pathlib.Path,
        help="List of search directories",
    )

    # Destination Arguments
    dest_args = parser.add_argument_group(
        "Destination",
        description="Output directory for matched files \nDirectory will be created if it does not exist",
    )
    # Forgoes destination as a postional argument
    # dest_args.add_argument('destination', nargs='?', help="Postional destination argument" )
    dest_args.add_argument(
        "-d",
        "--destination",
        action="store",
        nargs="?",
        type=pathlib.Path,
        help="Non positional argument for destination direcotory",
        default="./matched_files",
    )
    # Todo: Check for existing "matched_files" dir, if exist and is empty of files proceed
    # Todo... else add _1. Add flag to ignore this
    # Todo: What is ./ from? windows\powershell, windows\cmd? Otherwise, set default to PATH:SOURCE\matched_files

    # Action Arguments
    action_arg = parser.add_argument_group(
        "Action", "How to manage matched files \nOnly one argument is acceptible"
    )
    action_arg = action_arg.add_mutually_exclusive_group()
    action_arg.add_argument(
        "-m",
        "--move",
        help="Moves matched files",
        action="store_const",
        const="move",
        dest="action",
    )
    # TODO ===
    # * (DO ME) * move, copy, and to-file shall have same dest="action" (or smth), and whenever we need output we use -d
    # tho for easy use the --to-file .\dest\file is allowed as a suppliment to -d .\dest (and have this override the dest)
    action_arg.add_argument(
        "-c",
        "--copy",
        help="Copies matched files",
        action="store_const",
        const="copy",
        dest="action",
    )
    action_arg.add_argument(
        "--to-file",
        help="Output matched filepaths as a list to a file",
        dest="action",
        action="store_const",
        const="to_file",
    )
    # ? Add back to above? Testing things
    # type=pathlib.Path, nargs=1
    # Todo: To have an input after --to-file, write custom action function to in code add -d .\dest to parser
    # Todo... and set the action='to_file' etc. etc 

    # Miscellaneous Arguments
    misc_args = parser.add_argument_group(
        "Miscellaneous", description="Other optional arguments"
    )
    # misc_args.add_argument(
    #     "-",
    #     "--",
    #     action="store",
    #     nargs="?",
    #     help="Non positional argument for destination direcotory",
    #     default="./matched_files"
    # )

    args = parser.parse_args()
    print(args)

    # Todo: Apply your own 'usage' parameters. Like one for postional arguments only,
    # Todo... with destination, with only flags or with mixed
    # Todo: Add verbose, force, rename-options etc.


command_arguments()
