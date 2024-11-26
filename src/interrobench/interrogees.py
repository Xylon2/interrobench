"""
These are the mystery functions which the LLM will interrogate to find out what they do.
Each also has a set of verifications which the system will use to check the LLM gets it right.
"""

from string import ascii_lowercase
import statistics
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
def float_division(a: int, b: int) -> str | float:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a / b

interrogees.append({"name": "float division",
                    "function": float_division,
                    "verifications": [[1, 2], [4, 5], [45, 16]]})

@tool("test_function")
def is_odd(a: int) -> bool:
    """Use this tool to test the mystery function."""
    return a % 2 == 1

interrogees.append({"name": "is odd",
                   "function": is_odd,
                   "verifications": [[100], [13], [42], [93]]})

@tool("test_function")
def triangle_third_angle(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return 180 - a - b

interrogees.append({"name": "triangle third angle",
                   "function": triangle_third_angle,
                   "verifications": [[60, 60], [45, 45], [30, 60], [90, 45], [120, 30]]})

@tool("test_function")
def between_3_and_6(a: int) -> bool:
    """Use this tool to test the mystery function."""
    return 3 < a < 6

interrogees.append({"name": "between 3 and 6",
                   "function": between_3_and_6,
                   "verifications": [[2], [3], [5], [6], [7]]})

@tool("test_function")
def square(a: int) -> int:
    """Use this tool to test the mystery function."""
    return a * a

interrogees.append({"name": "square",
                   "function": square,
                   "verifications": [[2], [6], [10]]})

@tool("test_function")
def divide_by_4(a: int) -> float:
    """Use this tool to test the mystery function."""
    return a / 4

interrogees.append({"name": "divide by 4",
                   "function": divide_by_4,
                   "verifications": [[4], [8], [1], [16]]})

@tool("test_function")
def integer_division(a: int, b: int) -> str | int:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a // b

interrogees.append({"name": "integer division",
                    "function": integer_division,
                    "verifications": [[1, 2], [4, 5], [45, 16]]})

@tool("test_function")
def remainder(a: int, b: int) -> str | int:
    """Use this tool to test the mystery function."""
    return "Undefined" if b == 0 else a % b

interrogees.append({"name": "remainder",
                    "function": remainder,
                    "verifications": [[3, 2], [45, 16], [13, 13]]})

@tool("test_function")
def median(a: int, b: int, c: int, d: int, e: int) -> int:
    """Use this tool to test the mystery function."""
    return statistics.median([a, b, c, d, e])

interrogees.append({"name": "median of 5",
                    "function": median,
                    "verifications": [[1, 2, 3, 4, 5], [40, 15, 60, 3, 13], [0, 0, 0, 4, 400]]})

@tool("test_function")
def circle_circumference(a: int) -> float:
    """Use this tool to test the mystery function."""
    return 2 * 3.14159 * a

interrogees.append({"name": "circle circumference",
                   "function": circle_circumference,
                   "verifications": [[1], [5], [10], [0], [100]]})

@tool("test_function")
def find_higher(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    return max(a, b)

interrogees.append({"name": "find higher number",
                   "function": find_higher,
                   "verifications": [[10, 5], [3, 8], [-2, -5], [7, 7]]})

@tool("test_function")
def is_prime(a: int) -> bool:
    """Use this tool to test the mystery function."""
    if a < 2:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

interrogees.append({"name": "is prime",
                   "function": is_prime,
                   "verifications": [[2], [7], [4], [1], [13], [25]]})

@tool("test_function")
def concatenate_numbers(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return int(str(abs(a)) + str(abs(b)) + str(abs(c)))

interrogees.append({"name": "concatenate numbers",
                   "function": concatenate_numbers,
                   "verifications": [[1, 2, 3], [5, 10, 15], [42, 0, 7]]})

@tool("test_function")
def count_digits(a: int) -> int:
    """Use this tool to test the mystery function."""
    return len(str(abs(a)))

interrogees.append({"name": "count digits",
                   "function": count_digits,
                   "verifications": [[123], [5556], [0], [9]]})

@tool("test_function")
def difference_from_12_doubled(a: int) -> int:
    """Use this tool to test the mystery function."""
    return abs(12 - a) * 2

interrogees.append({"name": "difference from 12 doubled",
                   "function": difference_from_12_doubled,
                   "verifications": [[10], [14], [12], [0], [24], [-4]]})

@tool("test_function")
def ignore_one(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return a * c

interrogees.append({"name": "ignore one argument",
                    "function": ignore_one,
                    "verifications": [[3, 2, 9], [4, 5, 2], [0, 9, 3]]})

@tool("test_function")
def sum_bigger_than_9(a: int, b: int) -> bool:
    """Use this tool to test the mystery function."""
    return (a + b) > 9

interrogees.append({"name": "sum bigger than 9",
                   "function": sum_bigger_than_9,
                   "verifications": [[5, 5], [2, 3], [8, 2], [4, 5]]})

@tool("test_function")
def closest_pair_difference(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    diffs = [abs(a - b), abs(b - c), abs(a - c)]
    return min(diffs)

interrogees.append({"name": "difference of closest pair",
                   "function": closest_pair_difference,
                   "verifications": [[1, 5, 8], [10, 11, 15], [0, 7, 2], [4, 4, 8]]})

@tool("test_function")
def add_and_subtract(a: int, b: int, c: int) -> int:
    """Use this tool to test the mystery function."""
    return a + b - c

interrogees.append({"name": "add and subtract",
                    "function": add_and_subtract,
                    "verifications": [[5, 2, 3], [4, 5, 9], [25, 15, 1]]})

@tool("test_function")
def multiply_and_add(a: int, b: int, c: int) -> int:
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

@tool("test_function")
def times_3_round_5(a: int) -> int:
    """Use this tool to test the mystery function."""
    return round(a * 3 / 5) * 5

interrogees.append({"name": "times 3 round to nearest 5",
                   "function": times_3_round_5,
                   "verifications": [[10], [7], [3], [0], [15], [-4]]})

@tool("test_function")
def pythagorean(a: int, b: int) -> float:
    """Use this tool to test the mystery function."""
    return (a * a + b * b) ** 0.5

interrogees.append({"name": "pythagorean theorem",
                   "function": pythagorean,
                   "verifications": [[3, 4], [5, 12], [8, 15]]})

@tool("test_function")
def greatest_common_factor(a: int, b: int) -> int:
    """Use this tool to test the mystery function."""
    while b:
        a, b = b, a % b
    return abs(a)

interrogees.append({"name": "greatest common factor",
                   "function": greatest_common_factor,
                   "verifications": [[12, 18], [54, 24], [7, 13], [100, 25]]})

@tool("test_function")
def modulus_3_as_string(a: int) -> str:
    """Use this tool to test the mystery function."""
    fruits = {1: "apple", 2: "orange", 0: "banana"}
    return fruits[a % 3]

interrogees.append({"name": "modulus 3 as string",
                   "function": modulus_3_as_string,
                   "verifications": [[7], [5], [0], [15]]})

@tool("test_function")
def set_heading(a: int, b: int) -> str:
    """Use this tool to test the mystery function."""
    lat = 36
    long = 140

    vdiff = lat - a
    hdiff = long - b

    if vdiff == 0 and hdiff == 0:
        return "You've arrived!"
    
    if abs(vdiff) > abs(hdiff):
        return "North" if vdiff > 0 else "South"
    else:
        return "East" if hdiff > 0 else "West"

interrogees.append({"name": "set heading",
                   "function": set_heading,
                   "verifications": [[12, 18], [54, 144], [30, 144], [30, 150]]})

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
def count_vowels(a: str) -> int:
    """Use this tool to test the mystery function."""
    return sum(1 for char in a.lower() if char in 'aeiou')

interrogees.append({"name": "count vowels",
                   "function": count_vowels,
                   "verifications": [["hello"], ["aardvark"], ["rhythm"], ["Python"]]})

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
def minimum_five_chars(a: str) -> str | bool:
    """Use this tool to test the mystery function."""
    return a if len(a) >= 5 else False

interrogees.append({"name": "minimum five characters",
                   "function": minimum_five_chars,
                   "verifications": [["hello"], ["cat"], ["python"], [""], ["abcde"]]})

@tool("test_function")
def delete_second_and_reverse(a: str) -> str:
    """Use this tool to test the mystery function."""
    if len(a) < 2:
        return a
    return (a[0] + a[2:])[::-1]

interrogees.append({"name": "delete second letter and reverse",
                   "function": delete_second_and_reverse,
                   "verifications": [["hello"], ["python"], ["test"]]})

@tool("test_function")
def longest_common_substring(a: str, b: str) -> str:
    """Use this tool to test the mystery function."""
    if not a or not b:
        return ""
    m = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    longest, x_longest = 0, 0
    for x in range(len(a)):
        for y in range(len(b)):
            if a[x] == b[y]:
                m[x + 1][y + 1] = m[x][y] + 1
                if m[x + 1][y + 1] > longest:
                    longest = m[x + 1][y + 1]
                    x_longest = x + 1
    return a[x_longest - longest:x_longest]

interrogees.append({"name": "longest common substring",
                   "function": longest_common_substring,
                   "verifications": [["hello", "world"], ["python", "typhoon"], ["abcde", "cdefg"], ["cat", "hat"], ["", "test"]]})


# hard questions
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

@tool("test_function")
def crack_lock(a: int, b: int, c: int, d: int) -> int | str:
    """Use this tool to test the mystery function."""
    code = [5, 3, 8, 4]

    acc = 0
    for real, attempt in zip(code, [a, b, c, d]):
        acc += abs(real - attempt)

    if acc == 0:
        return "You got it!"
    else:
        return acc

interrogees.append({"name": "crack lock",
                    "function": crack_lock,
                    "verifications": [[1, 9, 7, 7], [9, 5, 9, 8], [4, 2, 1, 0]]})

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
