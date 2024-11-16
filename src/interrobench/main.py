import yaml
import os
from functools import reduce
from toolz.dicttoolz import update_in

# other modules
from interrogees import interrogees_
from shared import prompt_continue
from interrogate import interrogate
from verify import verify

# providers
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain_xai import ChatXAI

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    return config


def rfn(config, llm, msgfmt, acc, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]
    verifications = mystery_fn["verifications"]

    prompt_continue(config, "prompt-each-interrogation")
    print("\n### SYSTEM: interrogating function", name)

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    # run the interrogation
    messages = interrogate(config, llm_w_tool, mystery_fn, msgfmt)

    print("\n### SYSTEM: verifying function", name)
    # run the verification
    if verify(config, llm_wo_tool, messages, verifications, mystery_fn):
        return update_in(acc, ["score"], lambda n: n + 1)
    else:
        return update_in(acc, ["wrong"], lambda xs: xs + [name])

def main():
    config = load_config("resources/config.yaml") | load_config("resources/credentials.yaml")
    model = config["model"]
    api_keys = config["api-keys"]

    # prepare the appropriate runnable
    # https://python.langchain.com/docs/integrations/providers/
    match model["provider"]:
        case "openai":
            llm = ChatOpenAI(model=model["name"], api_key=api_keys["openai"])
            msgfmt = lambda x: x
        case "anthropic":
            llm = ChatAnthropic(model=model["name"], api_key=api_keys["anthropic"])
            msgfmt = lambda x: x["text"]
        case "google":
            # to make this work, I had to run these in bash:
            # $ gcloud config set project gcp-project-name
            # $ gcloud auth application-default login
            #
            # actually, it still doesn't seem to work correctly. may be a langchain bug
            llm = ChatVertexAI(model=model["name"], api_key=api_keys["google"])
            msgfmt = lambda x: x
        case "xai":
            llm = ChatXAI(model=model["name"], xai_api_key=api_keys["xai"])
            msgfmt = lambda x: x

    test_results = reduce(lambda a, b: rfn(config, llm, msgfmt, a, b), interrogees_, {"score": 0, "wrong": []})
            
    print("Final score:", test_results["score"])
    print("Wrong answers:", test_results["wrong"])

if __name__ == "__main__":
    main()
