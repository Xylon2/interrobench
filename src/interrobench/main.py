import yaml
from functools import reduce

# other modules
from interrogees import interrogees
from shared import prompt_continue
from interrogate import interrogate

# providers
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    return config

def rfn(config, llm, score, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]
    verifications = mystery_fn["verifications"]

    print("Interrogating function", name)
    prompt_continue(config, "prompt-each-interrogation")

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    # run the interrogation
    interrogate(config, llm_w_tool, mystery_fn)

    # run the verification
    print("verification stub")
    
    if True:
        return score + 1
    else:
        return score + 1

def main():
    config = load_config("resources/config.yaml") | load_config("resources/credentials.yaml")
    model = config["model"]
    api_keys = config["api-keys"]

    # prepare the appropriate runnable
    match model["provider"]:
        case "openai":
            llm = ChatOpenAI(model=model["name"], api_key=api_keys["openai"])
        case "anthropic":
            llm = ChatAnthropic(model=model["name"], api_key=api_keys["anthropic"])

    print("Final score:", reduce(lambda a, b: rfn(config, llm, a, b), interrogees, 0))

if __name__ == "__main__":
    main()
