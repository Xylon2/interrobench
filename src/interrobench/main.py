import yaml
from functools import reduce
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain_core.messages import HumanMessage, SystemMessage

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    return config

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

def main():
    config = load_config("resources/config.yaml") | load_config("resources/credentials.yaml")
    model = config["model"]
    api_keys = config["api-keys"]

    # prepare the appropriate runnable
    match model["provider"]:
        case "openai":
            model = ChatOpenAI(model=model["name"], api_key=api_keys["openai"])
        case "anthropic":
            model = ChatAnthropic(model=model["name"], api_key=api_keys["anthropic"])

    print(model.invoke(messages))

if __name__ == "__main__":
    main()
