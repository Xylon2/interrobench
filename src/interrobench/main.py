import os
from functools import reduce
import math

import yaml
from toolz.dicttoolz import update_in
from pydantic import ValidationError
from importlib.metadata import version
from datetime import datetime

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
from .shared import prompt_continue, AccumulatingPrinter
from .interrogate import interrogate, NoToolException, MsgLimitException
from .verify import verify, InvalidLLMOutputError

# db
import psycopg2
from pypika import Query, Table
import json

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

def interrogate_and_verify(config, llm_w_tool, llm_wo_tool, cursor, run_id, attempt_index, mystery_fn):
    name = mystery_fn["name"]
    verifications = mystery_fn["verifications"]

    start_time = datetime.now()

    # setup the printer
    printer = AccumulatingPrinter()

    printer.print("\n### SYSTEM: interrogating function", name)
    # run the interrogation
    messages, tool_call_count = interrogate(config, llm_w_tool, printer, mystery_fn)

    printer.print("\n### SYSTEM: verifying function", name)

    verification_result = verify(config, llm_wo_tool, messages, verifications, printer, mystery_fn)

    time_taken = (datetime.now() - start_time).total_seconds()
    attempt_data = {"run_id": run_id,
                    "function": name,
                    "result": verification_result,
                    "attempt_index": attempt_index,
                    "time_taken": time_taken,
                    "tool_calls": tool_call_count,
                    "complete_log": printer.retrieve()}

    insert_query = Query.into(Table("attempts")).columns(*attempt_data.keys()).insert(*attempt_data.values())
    cursor.execute(str(insert_query))

    return verification_result

def rfn(config, llm, cursor, run_id, acc, mystery_fn):
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
    loop_index = 0
    while not has_n_duplicates(required_wins, scores):
        try:
            result = interrogate_and_verify(config, llm_w_tool, llm_wo_tool, cursor, run_id, loop_index, mystery_fn)
            scores.append(result)
            if not result:
                failures.append("wrong answer")

        except (UnprocessableEntityError, MsgLimitException, NoToolException, InvalidLLMOutputError, ValidationError) as e:
            # these errors are considered to be the LLM's fault, so it will not get any points awarded
            print(e)
            scores.append(False)
            failures.append(type(e).__name__)

        loop_index += 1

    if most_common_element(scores):  # if more True than False
        print("\n### SYSTEM: best of", config["best-of"], "passed after", len(scores), "runs")
        return update_in(acc, ["score"], lambda n: n + 1)

    else:
        print("\n### SYSTEM: best of", config["best-of"], "failed after", len(scores), "runs")
        return update_in(acc, ["wrong"], lambda xs: xs + [(name, set(failures))])

def main():
    config_non_sensitive = load_config("resources/config.yaml")
    config = config_non_sensitive | load_config("resources/credentials.yaml")
    model = config["model"]
    api_keys = config["api-keys"]

    # connect to postgresql
    db_conn = psycopg2.connect(config["postgres-url"])
    cursor = db_conn.cursor()

    start_time = datetime.now()

    # we create the run table now even though we don't have all the data we need yet
    run_data = {"model_identifier": model["name"],
                "benchmark_version": version("interrobench").split('.', 1)[0],
                "config": json.dumps(config_non_sensitive),
                "datetime_start": start_time.strftime('%Y-%m-%d %H:%M:%S')
                }
    
    runs = Table("runs")
    insert_query = Query.into(runs).columns(*run_data.keys()).insert(*run_data.values())
    cursor.execute(str(insert_query) + " RETURNING id")
    run_id = cursor.fetchone()[0]

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

    test_results = reduce(lambda a, b: rfn(config, llm, cursor, run_id, a, b), interrogees_, {"score": 0, "wrong": []})

    print("\n### SYSTEM: tests complete for model `" + model["name"] + "`. Best of", config["best-of"])
    print("Final score:", test_results["score"], "/", len(interrogees_))
    print("Percent:", (test_results["score"] * 100) // len(interrogees_))
    print("Wrong answers:")
    print_aligned_tuples(test_results["wrong"])

    update_data = {"total_run_time": (datetime.now() - start_time).total_seconds(),
                   "final_score": json.dumps({"numerator": test_results["score"], "denominator": len(interrogees_)}),
                   "score_percent": (test_results["score"] * 100) // len(interrogees_)}

    for key, value in update_data.items():
        update_query = Query.update(runs).set(key, value).where(runs.id == run_id)
        cursor.execute(str(update_query))
    
    # Why do database libraries require so much boilerplate?
    db_conn.commit()
    cursor.close()
    db_conn.close()

if __name__ == "__main__":
    main()
