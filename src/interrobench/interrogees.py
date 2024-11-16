"""
These are the mystery functions which the LLM will interrogate to find out what they do.
Each also has a set of verifications which the system will use to check the LLM gets it right.
"""

from langchain.tools import tool
from string import ascii_lowercase
from toolz.dicttoolz import update_in

def list_to_alphabet_map(lst):
    """
    Maps a list to a dictionary with keys as sequential lowercase letters.
    
    :param lst: List of values to map
    :return: Dictionary with letters as keys
    """

    # Ensure the list is not longer than the available letters
    if len(lst) > len(ascii_lowercase):
        raise ValueError("List is too long to map to alphabetic letters.")

    return dict(zip(ascii_lowercase, lst))

def map_alphabet(xs):
    return [list_to_alphabet_map(x) for x in xs]

interrogees = []

# booleans
@tool("test_function")
def and_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a and b

interrogees.append({"name": "and",
                    "function": and_fn,
                    "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def or_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a or b

interrogees.append({"name": "or",
                    "function": or_fn,
                    "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def nand(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return not (a and b)

interrogees.append({"name": "nand",
                    "function": nand,
                    "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def xor(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return (a or b) and not (a and b)

interrogees.append({"name": "xor",
                    "function": xor,
                    "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def triple_and(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a and b and c

interrogees.append({"name": "triple and",
                    "function": triple_and,
                    "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_or(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a or b or c

interrogees.append({"name": "triple or",
                    "function": triple_or,
                    "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_nand(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return not (a and b and c)

interrogees.append({"name": "triple nand",
                    "function": triple_nand,
                    "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_xor(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return (sum([a, b, c]) % 2) == 1

interrogees.append({"name": "triple xor",
                    "function": triple_xor,
                    "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

# arithmetic
@tool("test_function")
def addition(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return a + b + c

interrogees.append({"name": "addition",
                    "function": addition,
                    "verifications": [[1, 2, 3], [4, 5, 6], [-1, 1, 0], [0, 0, 0]]})

@tool("test_function")
def subtraction(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a - b

interrogees.append({"name": "subtraction",
                    "function": subtraction,
                    "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})

@tool("test_function")
def multiplication(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a * b

interrogees.append({"name": "multiplication",
                    "function": multiplication,
                    "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})

@tool("test_function")
def integer_division(a: int, b: int) -> str:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a // b

interrogees.append({"name": "integer division",
                    "function": integer_division,
                    "verifications": [[1, 2], [4, 5], [45, 16]]})

@tool("test_function")
def remainder(a: int, b: int) -> str:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a % b

interrogees.append({"name": "remainder",
                    "function": remainder,
                    "verifications": [[1, 2], [4, 5], [45, 16], [13, 13]]})


# make it look the way langchain likes it
interrogees_ = [update_in(m, ["verifications"], map_alphabet) for m in interrogees]
