
# === IMPORTS ===

# CLI Argument handling
import argparse

# CLI argparse's path handling
import pathlib


# === CLI Argument Parsing ===

def cli_argparse():
    """ 
    Parsers the passed arguments and flags from a terminal interface when calling this program.
    """
    
    # Todo: We want the following
    # Postional: Source, Search
    # Non positional: Source, Search, Destination
    # Grouped Action Flags (only allow one): Copy, Move, --to-file:<path|| -d:path >
    # Misc arguments: quiet, verbose(include debug/log levels in code), force, dry-run (similar to --to-file but prints to terminal)
    # Add custom 'usage' parameters for a more understandible help menu
