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
    # Source,
    # Search...
    # Non positional:
    # Source:<path...>,
    # Search:<path...>,
    # Destination:<path...>
    # Grouped Action Flags (only allow one):
    # Copy,
    # Move,
    # --to-file:<path|| -d:path >
    # Misc arguments:
    # quiet,
    # verbose(include debug/log levels in code),
    # force (dunno for what),
    # dry-run (similar to --to-file but prints to terminal)
    # "dont-include-source-findings-except-for-matched-pairs" arguments (but a better name)

    # Initiates argparser
    # passed argumnet allows line/breaks in help text argument
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # -- Source Group --
    source_args = parser.add_argument_group(
        "Source",
        description="Source directory arguments. \nOne or multiple directories as a basis to compare files from \n",
    )
    source_args.add_argument(
        "source",
        action="store",
        nargs="?",
        # type=pathlib.Path,
        help="Single positional argument for source directory path",
    )
    source_args.add_argument(
        "-s",
        "--source",
        # action="append",
        nargs='+',
        # type=pathlib.Path,
        help="Specifies single or mulitple source direcetory paths",
    )
    args = parser.parse_args()
    
    # Dev: TEMP OUTPUT
    print(args)

# === RUNNING ===
command_line_interface_argument_parser()