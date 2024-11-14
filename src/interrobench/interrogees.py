"""
These are the mystery functions which the LLM will interrogate to find out what they do.
Each also has a set of verifications which the system will use to check the LLM gets it right.
"""

from langchain.tools import tool

functions = []

# booleans
@tool("test_function")
def and_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a and b

functions.append({"name": "and",
                  "function": and_fn,
                  "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def or_fn(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a or b

functions.append({"name": "or",
                  "function": or_fn,
                  "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def nand(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return not (a and b)

functions.append({"name": "nand",
                  "function": nand,
                  "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def xor(a: bool, b: bool) -> bool:
    """Use this tool to test the mystery function."""
    return (a or b) and not (a and b)

functions.append({"name": "xor",
                  "function": xor,
                  "verifications": [[True, True], [True, False], [False, True], [False, False]]})

@tool("test_function")
def triple_and(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a and b and c

functions.append({"name": "triple and",
                  "function": triple_and,
                  "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_or(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return a or b or c

functions.append({"name": "triple or",
                  "function": triple_or,
                  "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_nand(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return not (a and b and c)

functions.append({"name": "triple nand",
                  "function": triple_nand,
                  "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

@tool("test_function")
def triple_xor(a: bool, b: bool, c: bool) -> bool:
    """Use this tool to test the mystery function."""
    return (sum([a, b, c]) % 2) == 1

functions.append({"name": "triple xor",
                  "function": triple_xor,
                  "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]})

# arithmetic
@tool("test_function")
def addition(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return a + b + c

functions.append({"name": "addition",
                  "function": addition,
                  "verifications": [[1, 2, 3], [4, 5, 6], [-1, 1, 0], [0, 0, 0]]})

@tool("test_function")
def subtraction(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a - b

functions.append({"name": "subtraction",
                  "function": subtraction,
                  "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})

@tool("test_function")
def multiplication(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return a * b

functions.append({"name": "multiplication",
                  "function": multiplication,
                  "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})

@tool("test_function")
def integer_division(a: int, b: int) -> str:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a // b

functions.append({"name": "integer division",
                  "function": integer_division,
                  "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})

@tool("test_function")
def remainder(a: int, b: int) -> str:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a % b

functions.append({"name": "remainder",
                  "function": remainder,
                  "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]})