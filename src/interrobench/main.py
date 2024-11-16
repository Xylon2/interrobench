import yaml
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

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    return config


def rfn(config, llm, msgfmt, acc, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]
    verifications = mystery_fn["verifications"]

    prompt_continue(config, "prompt-each-interrogation")
    print("--- INTERROGATING FUNCTION", name, "---")

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    # run the interrogation
    messages = interrogate(config, llm_w_tool, mystery_fn, msgfmt)

    print("--- VERIFYING FUNCTION", name, "---")
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
    match model["provider"]:
        case "openai":
            llm = ChatOpenAI(model=model["name"], api_key=api_keys["openai"])
            msgfmt = lambda x: x
        case "anthropic":
            llm = ChatAnthropic(model=model["name"], api_key=api_keys["anthropic"])
            msgfmt = lambda x: x["text"]

    test_results = reduce(lambda a, b: rfn(config, llm, msgfmt, a, b), interrogees_, {"score": 0, "wrong": []})
            
    print("Final score:", test_results["score"])
    print("Wrong answers:", test_results["wrong"])

if __name__ == "__main__":
    main()
