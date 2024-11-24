import shutil
import textwrap
import sys

class AbortException(Exception):
    """Custom exception for user aborting the operation."""
    pass

def prompt_continue(config, key):
    if key in config["debug"]:
        while True:
            choice = input("Do you want to continue? (y/n): ").strip().lower()
            match choice:
                case 'y' | 'yes':
                    return True
                case 'n' | 'no':
                    raise AbortException("User chose to abort.")
                case _:
                    print("Please enter 'y' for yes or 'n' for no.")

class AccumulatingPrinter:
    def __init__(self):
        # Initialize the internal "megastring"
        self.megastring = ""

    def print(self, *args):
        """
        Prints the concatenated string from the arguments and appends it to the megastring.
        """
        # Concatenate arguments with spaces
        concatenated_string = " ".join(str(arg) for arg in args)
        
        # Print the concatenated string
        print(concatenated_string)
        
        # Append the concatenated string to the megastring
        self.megastring += concatenated_string + "\n"

    def indented_print(self, *args):
        """
        Prints an indented and wrapped version of the concatenated string from the arguments,
        and appends it to the megastring.
        """
        # Concatenate arguments with spaces
        concatenated_string = " ".join(str(arg) for arg in args)

        # Get terminal width and calculate wrap width
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        wrap_width = max(terminal_width - 5, 10)  # Ensure wrap width isn't too narrow

        # Wrap the string and add indentation
        wrapped_lines = textwrap.fill(concatenated_string, width=wrap_width, subsequent_indent="  ", initial_indent="  ")

        # Print the indented string
        print(wrapped_lines)

        # Append the wrapped and indented string to the megastring
        self.megastring += wrapped_lines + "\n"

    def retrieve(self):
        """
        Returns the accumulated megastring.
        """
        return self.megastring
