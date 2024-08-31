# === IMPORTS ===

# CLI Argument handling
import argparse

# CLI argparse's path handling
import pathlib


# === CLI Argument Parsing ===


def command_line_interface_argument_parser():
    """
    Parsers the passed arguments and flags from a terminal interface when calling this program.
    """

    # Todo: Checklist
    # Add custom 'usage' parameters for a more understadible help menu

    # Todo: Arguments
    # Postional:
    #   Source,
    #   Search...
    # Non positional:
    #   Source:<path...>,
    #   Search:<path...>,
    #   Destination:<path...>
    # Grouped Action Flags (only allow one):
    #   Copy,
    #   Move,
    #   --to-file:<path|| -d:path >
    # Misc arguments:
    #   quiet,
    #   verbose(include debug/log levels in code),
    #   force? (dunno for what, maybe as in ignore duplicates and overwrite),
    #   dry-run (similar to --to-file but prints to terminal)
    #   "dont-include-source-findings-except-for-matched-pairs" arguments (but a better name)
    #   duplicate-handling (overwrite/auto-extention/manual-comparision/idk)
    # #

    # Initiates argparser
    # passed argumnet allows line/breaks in help text argument
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # // ! Changed in version 3.11:
    # // ! Calling add_argument_group() on an argument group is deprecated.
    # // ! This feature was never supported and does not always work correctly.
    # // ! The function exists on the API by accident through inheritance and will be removed in the future.
    # // ! https://docs.python.org/3/library/argparse.html#argument-groups
    # * Note: Groups are not depricated, just groupcall ontop of groups

    #   Argument order by DOCs
    #   ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])

    # -- Source Group --
    source_args = parser.add_argument_group(
        "Source",
        description="Source directory arguments. \nOne or multiple directories as a basis to compare files from\n",
    )
    source_args.add_argument(
        "source",
        action="extend",
        nargs="?",
        help="Single positional argument for source directory path",
    )
    source_args.add_argument(
        "-S",
        "--source",
        action="extend",
        nargs="+",
        help="Specifies single or mulitple source direcetory paths",
    )

    # --- Search Group ---
    search_args = parser.add_argument_group(
        "Search",
        "Search directory arguments. \nOne or multiple directories to search for files in of\n",
    )
    search_args.add_argument(
        "search",
        action="extend",
        nargs="*",
        help="Single positional argument for source directory path",
    )
    search_args.add_argument(
        "-s",
        "--search",
        action="extend",
        nargs="+",
        help="Specifies single or mulitple search direcetory paths",
    )

    args = parser.parse_args()

    # Dev: TEMP OUTPUT
    print(args)


# === RUNNING ===
command_line_interface_argument_parser()
