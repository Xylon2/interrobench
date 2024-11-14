"""
These are the mystery functions which the LLM will interrogate to find out what they do.
Each also has a set of verifications which the system will use to check the LLM gets it right.
"""

interrogees = [
    # booleans
    {"name": "and",
     "args": ["boolean", "boolean"],
     "function": lambda a, b: a and b,
     "verifications": [[True, True], [True, False], [False, True], [False, False]]},

    {"name": "or",
     "args": ["boolean", "boolean"],
     "function": lambda a, b: a or b,
     "verifications": [[True, True], [True, False], [False, True], [False, False]]},

    {"name": "nand",
     "args": ["boolean", "boolean"],
     "function": lambda a, b: not (a and b),
     "verifications": [[True, True], [True, False], [False, True], [False, False]]},

    {"name": "xor",
     "args": ["boolean", "boolean"],
     "function": lambda a, b: (a or b) and not (a and b),
     "verifications": [[True, True], [True, False], [False, True], [False, False]]},

    {"name": "triple and",
     "args": ["boolean", "boolean", "boolean"],
     "function": lambda a, b, c: a and b and c,
     "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]},

    {"name": "triple or",
     "args": ["boolean", "boolean", "boolean"],
     "function": lambda a, b, c: a or b or c,
     "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]},

    {"name": "triple nand",
     "args": ["boolean", "boolean", "boolean"],
     "function": lambda a, b, c: not (a and b and c),
     "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]},

    {"name": "triple xor",
     "args": ["boolean", "boolean", "boolean"],
     "function": lambda a, b, c: (sum([a, b, c]) % 2) == 1,
     "verifications": [[True, True, True], [True, True, False], [True, False, True], [False, True, True]]},

    # arithmetic
    {"name": "addition",
     "args": ["integer", "integer", "integer"],
     "function": lambda a, b, c: a + b + c,
     "verifications": [[1, 2, 3], [4, 5, 6], [-1, 1, 0], [0, 0, 0]]},

    {"name": "subtraction",
     "args": ["integer", "integer"],
     "function": lambda a, b: a - b,
     "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]},

    {"name": "multiplication",
     "args": ["integer", "integer"],
     "function": lambda a, b: a * b,
     "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]},

    {"name": "integer division",
     "args": ["integer", "integer"],
     "function": lambda a, b: "Undefined" if b == 0 else a // b,
     "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]},

    {"name": "remainder",
     "args": ["integer", "integer"],
     "function": lambda a, b: "Undefined" if b == 0 else a % b,
     "verifications": [[1, 2], [4, 5], [-1, 1], [0, 0]]},
]
