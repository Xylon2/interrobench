import time
import sys
import shutil
import textwrap
from typing import Callable
from anthropic import InternalServerError
from google.api_core.exceptions import ResourceExhausted
from groq import RateLimitError
from httpx import ReadTimeout

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

class LLMRateLimiter:
    def __init__(self, rate_limit_seconds: int):
        """
        Initialize the RateLimiter.

        :param rate_limit_seconds: The initial number of seconds for the rate limit.
        """
        self.rate_limit_seconds = rate_limit_seconds
        self.last_call_time = None
        self.total_call_count = 0

    def __call__(self, llm: Callable, messages: list):
        """
        Call the LLM while enforcing the rate limit.
        """

        self.total_call_count += 1

        current_time = time.time()
        if self.last_call_time is not None:
            elapsed_time = current_time - self.last_call_time
            sleep_time = self.rate_limit_seconds - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.last_call_time = time.time()

        try:
            # Call the function
            return llm.invoke(messages)
        except (InternalServerError, ResourceExhausted, RateLimitError, ReadTimeout) as e:
            print()
            print(e)

            self.rate_limit_seconds += 1
            print(f"\n### SYSTEM: backing off for 5 minutes and increasing rate limit to {self.rate_limit_seconds} seconds")
            time.sleep(300)

            self.last_call_time = time.time()
            return llm.invoke(messages)
