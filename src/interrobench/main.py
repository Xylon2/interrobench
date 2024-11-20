import os
from functools import reduce
import math

import yaml
from toolz.dicttoolz import update_in
from pydantic import ValidationError

# providers
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain_xai import ChatXAI
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from cohere import UnprocessableEntityError

# other modules
from .interrogees import interrogees_
from .shared import prompt_continue
from .interrogate import interrogate, NoToolException, MsgLimitException
from .verify import verify, InvalidLLMOutputError

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    # Ensure "debug" is always a list
    if "debug" in config:
        if config["debug"] is None:
            config["debug"] = []

    return config

def print_aligned_tuples(tuple_list):
    if not tuple_list:
        return

    # Find the maximum length of the first elements
    max_length = max(len(t[0]) for t in tuple_list)

    # Print each tuple with proper alignment
    for first, second in tuple_list:
        print(f"  {first:<{max_length}}  {second}")

def has_n_duplicates(n, bool_list):
    """Ensure the list contains at least n of either True or False"""
    return bool_list.count(True) >= n or bool_list.count(False) >= n

class EqualCountError(Exception):
    """Exception raised when True and False have equal counts in the list."""
    pass

def most_common_element(bool_list):
    """return the most common element in the list"""
    count_true = bool_list.count(True)
    count_false = bool_list.count(False)

    if count_true > count_false:
        return True
    elif count_false > count_true:
        return False
    else:
        raise EqualCountError("True and False occur equally in the list.")

def interrogate_and_verify(config, llm_w_tool, llm_wo_tool, mystery_fn):
    name = mystery_fn["name"]
    verifications = mystery_fn["verifications"]

    print("\n### SYSTEM: interrogating function", name)
    # run the interrogation
    messages = interrogate(config, llm_w_tool, mystery_fn)

    print("\n### SYSTEM: verifying function", name)

    return verify(config, llm_wo_tool, messages, verifications, mystery_fn)

def rfn(config, llm, acc, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]

    prompt_continue(config, "prompt-each-interrogation")
    print("\n######################################################")
    print("### SYSTEM: testing function", name)
    print("######################################################")

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    required_wins = math.ceil(config["best-of"] / 2)

    scores = []
    failures = []
    while not has_n_duplicates(required_wins, scores):
        try:
            result = interrogate_and_verify(config, llm_w_tool, llm_wo_tool, mystery_fn)
            scores.append(result)
            if not result:
                failures.append("wrong answer")

        except (UnprocessableEntityError, MsgLimitException, NoToolException, InvalidLLMOutputError, ValidationError) as e:
            # these errors are considered to be the LLM's fault, so it will not get any points awarded
            print(e)
            scores.append(False)
            failures.append(type(e).__name__)

    if most_common_element(scores):  # if more True than False
        print("\n### SYSTEM: best of", config["best-of"], "passed after", len(scores), "runs")
        return update_in(acc, ["score"], lambda n: n + 1)

    else:
        print("\n### SYSTEM: best of", config["best-of"], "failed after", len(scores), "runs")
        return update_in(acc, ["wrong"], lambda xs: xs + [(name, set(failures))])

def main():
    config = load_config("resources/config.yaml") | load_config("resources/credentials.yaml")
    model = config["model"]
    api_keys = config["api-keys"]

    # prepare the appropriate runnable
    # https://python.langchain.com/docs/integrations/providers/
    match model["provider"]:
        case "openai":
            llm = ChatOpenAI(model=model["name"], api_key=api_keys["openai"])
        case "anthropic":
            llm = ChatAnthropic(model=model["name"], api_key=api_keys["anthropic"])
        case "cohere":
            os.environ["COHERE_API_KEY"] = api_keys["cohere"]
            llm = ChatCohere(model=model["name"], co_api_key=api_keys["cohere"])
        case "xai":
            llm = ChatXAI(model=model["name"], xai_api_key=api_keys["xai"])
        case "groq":
            llm = ChatGroq(model=model["name"], api_key=api_keys["groq"])
        case "google":
            # to make this work, I had to run these in bash:
            # $ gcloud config set project gcp-project-name
            # $ gcloud auth application-default login
            #
            # actually, it still doesn't seem to work correctly. may be a langchain bug
            llm = ChatVertexAI(model=model["name"], api_key=api_keys["google"])

    if "easy-tests-only" in config["debug"]:
        print("SHORT_TEST")
        interrogees_[:] = interrogees_[:3]

    elif "hard-tests-only" in config["debug"]:
        print("SHORT_TEST")
        interrogees_[:] = interrogees_[-3:]

    test_results = reduce(lambda a, b: rfn(config, llm, a, b), interrogees_, {"score": 0, "wrong": []})

    print("\n### SYSTEM: tests complete for model `" + model["name"] + "`. Best of", config["best-of"])
    print("Final score:", test_results["score"], "/", len(interrogees_))
    print("Percent:", (test_results["score"] * 100) // len(interrogees_))
    print("Wrong answers:")
    print_aligned_tuples(test_results["wrong"])

if __name__ == "__main__":
    main()
