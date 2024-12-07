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
from groq import BadRequestError

# other modules
from .interrogees import interrogees_
from .shared import prompt_continue, AccumulatingPrinter, LLMRateLimiter
from .interrogate import interrogate, NoToolException, MsgLimitException
from .verify import verify

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

def interrogate_and_verify(config, llm_w_tool, llm_wo_tool, rate_limiter, cursor, run_id, attempt_index, mystery_fn):
    name = mystery_fn["name"]
    verifications = mystery_fn["verifications"]

    start_time = datetime.now()
    start_api_calls = rate_limiter.total_call_count

    # setup the printer
    printer = AccumulatingPrinter()

    try:
        printer.print("\n### SYSTEM: interrogating function", name)
        messages, tool_call_count = interrogate(config, llm_w_tool, rate_limiter, printer, mystery_fn)

        printer.print("\n### SYSTEM: verifying function", name)
        verification_result = verify(config, llm_wo_tool, rate_limiter, messages, verifications, printer, mystery_fn)

    except (UnprocessableEntityError, MsgLimitException, NoToolException, ValidationError, BadRequestError) as e:
        # these errors are considered to be the LLM's fault, so it will not get any points awarded
        printer.print("\n### SYSTEM: The following Error occured:")
        printer.print(e)
        verification_result = type(e).__name__
        tool_call_count = None

    time_taken = (datetime.now() - start_time).total_seconds()
    attempt_data = {"run_id": run_id,
                    "function": name,
                    "result": verification_result,
                    "attempt_index": attempt_index,
                    "time_taken": time_taken,
                    "tool_calls": tool_call_count,
                    "complete_log": printer.retrieve(),
                    "api_calls": rate_limiter.total_call_count - start_api_calls}

    insert_query = Query.into(Table("attempts")).columns(*attempt_data.keys()).insert(*attempt_data.values())
    cursor.execute(str(insert_query))

    return verification_result

def rfn(config, llm, rate_limiter, cursor, run_id, acc, mystery_fn):
    name = mystery_fn["name"]
    function = mystery_fn["function"]
    attempts = config["attempts"]

    prompt_continue(config, "pause-each-interrogation")
    print("\n######################################################")
    print("### SYSTEM: testing function", name)
    print("######################################################")

    llm_wo_tool = llm
    llm_w_tool = llm.bind_tools([function])

    score = 0

    for i in range(attempts):
        result = interrogate_and_verify(config, llm_w_tool, llm_wo_tool, rate_limiter, cursor, run_id, i, mystery_fn)
        if result == True:
            score += 1

    print("\n### SYSTEM: passed", score, "/", attempts, "attempts")
    return acc + score

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
            llm = ChatOpenAI(model=model["name"],
                             api_key=api_keys["openai"])
        case "anthropic":
            llm = ChatAnthropic(model=model["name"],
                                api_key=api_keys["anthropic"])
        case "cohere":
            os.environ["COHERE_API_KEY"] = api_keys["cohere"]
            llm = ChatCohere(model=model["name"],
                             co_api_key=api_keys["cohere"])
        case "xai":
            llm = ChatXAI(model=model["name"],
                          xai_api_key=api_keys["xai"])
        case "google":
            # to make this work, I had to run these in bash:
            # $ gcloud config set project gcp-project-name
            # $ gcloud auth application-default login
            llm = ChatVertexAI(model=model["name"],
                               api_key=api_keys["google"],
                               max_retries=3)
        case "groq":
            llm = ChatGroq(model=model["name"],
                           api_key=api_keys["groq"])

    # fetch the configured subset of the problems
    interrogees = list(filter(lambda d: config["problem-set"] in d.get("tags", set()), interrogees_))

    rate_limiter = LLMRateLimiter(rate_limit_seconds=config['rate-limit'])

    score = reduce(lambda a, b: rfn(config, llm, rate_limiter, cursor, run_id, a, b), interrogees, 0)

    percent = (score * 100) // (len(interrogees) * config["attempts"])

    print("\n### SYSTEM: run complete for model `" + model["name"] + "`.")
    print("Final score:", score, "/", len(interrogees) * config["attempts"])
    print("Percent:", percent)
    print("Wrong answers:")

    attempts = Table("attempts")
    get_wrong_query = Query.from_(attempts).select(attempts.function, attempts.result).where(attempts.run_id == run_id).where(attempts.result != 'true')

    cursor.execute(str(get_wrong_query))
    wrong = cursor.fetchall()

    # we want to print the wrong results per function. so get it from the db
    wrong_list = []
    for target_function in {t[0] for t in wrong}:
        results = [result for function, result in wrong if function == target_function]

        wrong_list.append((target_function, results))

    print_aligned_tuples(wrong_list)

    update_data = {"total_run_time": (datetime.now() - start_time).total_seconds(),
                   "final_score": json.dumps({"numerator": score, "denominator": len(interrogees) * config["attempts"]}),
                   "score_percent": percent,
                   "total_api_calls": rate_limiter.total_call_count}

    for key, value in update_data.items():
        update_query = Query.update(runs).set(key, value).where(runs.id == run_id)
        cursor.execute(str(update_query))

    # Why do database libraries require so much boilerplate?
    db_conn.commit()
    cursor.close()
    db_conn.close()

if __name__ == "__main__":
    main()
