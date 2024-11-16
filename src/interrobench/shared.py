import shutil
import textwrap
import sys

class AbortException(Exception):
    """Custom exception for user aborting the operation."""
    pass

def prompt_continue(config, key):
    if config["debug"] == None:
        return

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

def indented_print(*args, sep=" ", end="\n", **kwargs):
    """
    Custom print function that prepends two spaces to every line,
    wraps lines to terminal width - 5, and supports multi-line strings.
    """
    # Determine the terminal width, defaulting to 80 if unavailable
    terminal_width = shutil.get_terminal_size((80, 20)).columns - 5
    wrapper = textwrap.TextWrapper(width=terminal_width, subsequent_indent="  ", initial_indent="  ")

    # Combine all args into a single string as the built-in print would
    output = sep.join(str(arg) for arg in args)

    # Split the output into lines, wrap each line, and prepend two spaces
    wrapped_output = "\n".join(wrapper.fill(line) for line in output.splitlines())

    # Print the wrapped output
    sys.stdout.write(wrapped_output + end)
