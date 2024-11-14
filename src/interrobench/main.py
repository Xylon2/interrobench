import yaml
from functools import reduce
from langchain_openai import ChatOpenAI

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    return config

def add(x, y):
    return x + y

def main():
    config = load_config("resources/config.yaml") | load_config("resources/credentials.yaml")

    print(config)

    numbers = [1, 2, 3, 4, 5]
    result = reduce(add, numbers)
    print(result)

if __name__ == "__main__":
    main()
