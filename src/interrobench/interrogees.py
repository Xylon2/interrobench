"""
These are the mystery functions which the LLM will interrogate to find out what they do.
Each also has a set of verifications which the system will use to check the LLM gets it right.
"""

from string import ascii_lowercase
from langchain.tools import tool
from toolz.dicttoolz import update_in

interrogees = []

# booleans
@tool("test_function")
def and_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a and b

interrogees.append({"name": "and",
                    "function": and_fn,
                    "verifications": [[True, True], [True, False], [False, False]]})

@tool("test_function")
def or_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a or b

interrogees.append({"name": "or",
                    "function": or_fn,
                    "verifications": [[True, True], [True, False], [False, False]]})

@tool("test_function")
def nand(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return not (a and b)

interrogees.append({"name": "nand",
                    "function": nand,
                    "verifications": [[True, True], [True, False], [False, False]]})

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
                    "verifications": [[1, 2, 3], [4, 5, 6], [0, 0, 0]]})

@tool("test_function")
def subtraction(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a - b

interrogees.append({"name": "subtraction",
                    "function": subtraction,
                    "verifications": [[10, 2], [7, 5], [1, 0]]})

@tool("test_function")
def multiplication(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a * b

interrogees.append({"name": "multiplication",
                    "function": multiplication,
                    "verifications": [[3, 2], [4, 5], [0, 9]]})

@tool("test_function")
def ignore_one(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return a * c

interrogees.append({"name": "ignore one argument",
                    "function": ignore_one,
                    "verifications": [[3, 2, 9], [4, 5, 2], [0, 9, 3]]})

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
                    "verifications": [[3, 2], [45, 16], [13, 13]]})

@tool("test_function")
def add_and_subtract(a: int, b: int, c: int) -> str:
    """Use this tool to test the mystery function."""
    return a + b - c

interrogees.append({"name": "add and subtract",
                    "function": add_and_subtract,
                    "verifications": [[5, 2, 3], [4, 5, 9], [25, 15, 1]]})

@tool("test_function")
def multiply_and_add(a: int, b: int, c: int) -> str:
    """Use this tool to test the mystery function."""
    return a * b + c

interrogees.append({"name": "multiply and add",
                    "function": multiply_and_add,
                    "verifications": [[1, 2, 7], [4, 5, 3], [3, 9, 8]]})

@tool("test_function")
def subtract_and_divide(a: int, b: int, c: int) -> str:
    """Use this tool to test the mystery function."""
    return "Undefined" if c == 0 else (a - b) // c

interrogees.append({"name": "subtract and divide",
                    "function": subtract_and_divide,
                    "verifications": [[10, 2, 2], [35, 16, 4], [13, 3, 5]]})

# string manipulations
@tool("test_function")
def remove_last_letter(a: str) -> str:
    """Use this tool to test the mystery function."""
    return a[:-1]

interrogees.append({"name": "remove last letter",
                    "function": remove_last_letter,
                    "verifications": [["hello"], ["world"]]})

@tool("test_function")
def concatenate(a: str, b: str) -> str:
    """Use this tool to test the mystery function."""
    return a + b

interrogees.append({"name": "concatenate",
                    "function": concatenate,
                    "verifications": [["banana", "potato"], ["bar", "foo"]]})

@tool("test_function")
def reverse_string(a: str) -> str:
    """Use this tool to test the mystery function."""
    return a[::-1]

interrogees.append({"name": "reverse string",
                    "function": reverse_string,
                    "verifications": [["hello"], ["world"], ["abcde"]]})

@tool("test_function")
def uppercase_string(a: str) -> str:
    """Use this tool to test the mystery function."""
    return a.upper()

interrogees.append({"name": "uppercase string",
                    "function": uppercase_string,
                    "verifications": [["hello"], ["world"], ["abc"]]})

@tool("test_function")
def string_length(a: str) -> int:
    """Use this tool to test the mystery function."""
    return len(a)

interrogees.append({"name": "string length",
                    "function": string_length,
                    "verifications": [["hello"], ["world"], ["abcdefg"]]})

@tool("test_function")
def repeat_string(a: str, b: int) -> str:
    """Use this tool to test the mystery function."""
    return a * b

interrogees.append({"name": "repeat string",
                    "function": repeat_string,
                    "verifications": [["hello", 3], ["abc", 5]]})

@tool("test_function")
def count_es(a: str) -> str:
    """Use this tool to test the mystery function."""
    return a.count('e')

interrogees.append({"name": "count e's",
                    "function": count_es,
                    "verifications": [["hello"], ["world"], ["the quick brown fox jumped over the lazy dog"]]})

@tool("test_function")
def contains_substring(a: str, b: str) -> bool:
    """Use this tool to test the mystery function."""
    return b in a

interrogees.append({"name": "contains substring",
                    "function": contains_substring,
                    "verifications": [["hello world", "world"], ["foobar", "bar"], ["abc", "d"]]})

###

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

# make it look the way langchain likes it
interrogees_ = [update_in(m, ["verifications"], map_alphabet) for m in interrogees]

# wishlist
# - median of 5 values?
