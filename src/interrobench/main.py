import yaml
import os
from functools import reduce
from toolz.dicttoolz import update_in

# other modules
from interrogees import interrogees_
from shared import prompt_continue
from interrogate import interrogate, NoToolException, MsgLimitException
from verify import verify

# providers
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain_xai import ChatXAI
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from cohere import UnprocessableEntityError

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

def rfn(config, llm, acc, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]
    verifications = mystery_fn["verifications"]

    prompt_continue(config, "prompt-each-interrogation")
    print("\n######################################################")
    print("### SYSTEM: interrogating function", name)
    print("######################################################")

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    # run the interrogation
    try:
        messages = interrogate(config, llm_w_tool, mystery_fn)
    except (UnprocessableEntityError, MsgLimitException, NoToolException) as e:
        print(e)
        return update_in(acc, ["wrong"], lambda xs: xs + [(name, type(e).__name__)])

    print("\n### SYSTEM: verifying function", name)
    # run the verification
    if verify(config, llm_wo_tool, messages, verifications, mystery_fn):
        return update_in(acc, ["score"], lambda n: n + 1)
    else:
        return update_in(acc, ["wrong"], lambda xs: xs + [(name, "wrong answer")])

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
            # doesn't work due to UnprocessableEntityError
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

    print("\n### SYSTEM: tests complete for model", model["name"])
    print("Ran", len(interrogees_), "tests.")
    print("Final score:", test_results["score"])
    print("Wrong answers:")
    print_aligned_tuples(test_results["wrong"])

if __name__ == "__main__":
    main()
