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
        and appends it to the megastring, preserving input newlines.
        """
        # Concatenate arguments with spaces
        concatenated_string = " ".join(str(arg) for arg in args)

        # Get terminal width and calculate wrap width
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        wrap_width = max(terminal_width - 5, 10)  # Ensure wrap width isn't too narrow

        # Split the string into lines to preserve existing newlines
        lines = concatenated_string.splitlines()
        wrapped_lines = []
        for line in lines:
            # Wrap each line individually and prepend indentation
            wrapped_lines.append(textwrap.fill(line, width=wrap_width, subsequent_indent="  ", initial_indent="  "))

        # Combine wrapped lines back into a single string
        indented_string = "\n".join(wrapped_lines)

        # Print the indented string
        print(indented_string)

        # Append the indented string to the megastring
        self.megastring += indented_string + "\n"

    def retrieve(self):
        """
        Returns the accumulated megastring.
        """
        return self.megastring
