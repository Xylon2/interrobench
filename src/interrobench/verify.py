from itertools import tee

from .shared import prompt_continue, llm_w_backoff

from typing_extensions import Annotated, TypedDict

class InvalidLLMOutputError(Exception):
    """Custom exception for invalid LLM output."""
    def __init__(self, message):
        super().__init__(message)

def validate_llmout(llmout):
    """Check if `llmout` is a dict with the required keys"""
    if not isinstance(llmout, dict):
        raise InvalidLLMOutputError("llmout must be a dictionary.")

    required_keys = {"thoughts", "expected_output"}
    if not required_keys.issubset(llmout.keys()):
        missing_keys = required_keys - llmout.keys()
        raise InvalidLLMOutputError(f"Missing keys in llmout: {', '.join(missing_keys)}")

def map_to_multiline_string(data: dict) -> str:
    "print the input arguments in a nice string format for the LLM"
    return "\n".join(f"{key}: {value}" for key, value in data.items())

def make_schema(eo_type):
    class Prediction(TypedDict):
        """Prediction of the function output."""

        thoughts: Annotated[str, ..., "explain your workings"]
        expected_output: Annotated[eo_type, ..., "the expected output from the function"]

    return Prediction

def prompt_maker(f_input):
    formatted =  map_to_multiline_string(f_input)

    return f"""To test your theory, please tell me what is the expected output from the function with this input:

{formatted}

You no-longer have access to the tool because I am testing if you have got it right.

Please respond in JSON with two keys: \"thoughts\" and \"expected_output\".
The expected_output key will be used automatically to check your results so only include the output you expect from the function. And use the thoughts key to explain your workings."""

def verify(config, llm, messages, verifications, printer, mystery_fn):
    # We will loop through the verifications. For each, we prompt the LLM and
    # check it's response. The first one it gets wrong, we abort.

    # tee because of how these iterators work I can't see the first item without consuming it
    expected_outputs, eo = tee(map(mystery_fn["function"].invoke, verifications))

    expected_type = type(next(eo))
    output_schema = make_schema(expected_type)
    llm_ = llm.with_structured_output(output_schema)

    for in_, out in zip(verifications, expected_outputs):
        #print("in:", in_)
        #print("out:", out)

        printer.print("\n### SYSTEM: inputs:")
        printer.indented_print(map_to_multiline_string(in_))

        # amnesia between tests is fine
        llmout = llm_w_backoff(llm_, messages + [prompt_maker(in_)])

        validate_llmout(llmout)

        printer.print("\n--- LLM ---")
        printer.indented_print(llmout["thoughts"], "\n")
        printer.print()
        printer.indented_print("`" + str(llmout["expected_output"]) + "`\n")

        prompt_continue(config, "prompt-each-message")

        if llmout["expected_output"] == out:
            printer.print("\n### SYSTEM: CORRECT")
        else:
            printer.print("\n### SYSTEM: WRONG")
            return False

    # if we got here all the verifications passed
    return True
