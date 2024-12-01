# InterroBench
[![Python application](https://github.com/Xylon2/interrobench/actions/workflows/python-app.yml/badge.svg)](https://github.com/Xylon2/interrobench/actions/workflows/python-app.yml)

## Intro

InterroBench is a novel benchmark for LLMs.

Each test is a conversation where the AI has to interrogate a mystery
function to find out what it does.

This is done using the "tool use" or "function calling" features that
most LLMs provide. The LLM can call the tool as many times as it wants
to test the function and figure-out what it does.

When the LLM is confident it has figured it out, then the system tests the LLM
got it right by asking it what output it would expect the function to provide
from a given input.

If you want to see the results: see [The LeaderBoard](https://interrobench.com/).

## Running

If you want to run this benchmark yourself, you will need:
- An account and API key for whichever LLM provider you want to use
- A computer to install Python and PostgreSQL on. Postgres is how it stores analytics for each run

General instructions follow. Alternatively you may watch this video for Ubuntu instructions: [Installing and Running InterroBench on Ubuntu](https://youtu.be/gqIXEt2TBoI).

Checkout this code.

Install these:
- PostgreSQL
  - server
  - client
  - libpq-dev
- Python3:
  - runtime
  - pip
  - virtualenv

Create a postgresql database and user.

Create a couple of config files:

A `resources/config.yaml` should look like this (uncomment sections as appropriate):
```
---

msg-limit: 30    # the number of requests the tool can use per attempt
rate-limit: 5    # seconds between requests
best-of: 5       # how many times is each function tested
model: {name: "claude-3-5-haiku-20241022", provider: "anthropic"}
#model: {name: "gpt-4o-mini-2024-07-18", provider: "openai"}
#model: {name: "grok-beta", provider: "xai"}
#model: {name: "gemini-1.5-flash", provider: "google"}
#model: {name: "command-r-plus", provider: "cohere"}
#model: {name: "llama3-groq-70b-8192-tool-use-preview", provider: "groq"}

debug:
#  - pause-each-interrogation
#  - pause-each-message
#  - easy-problems-only
#  - hard-problems-only
```

And a `resources/credentials.yaml` containing your db credentials and API keys:
```
---

postgres-url: "postgresql://user:password@localhost/dbname"
api-keys:
  anthropic: ""
  openai: ""
  xai: ""
  cohere: ""
```

Running it should be essentially:
- make a virtualenv and activate it
- install interrobench into your virtualenv with `pip install -e .`
- run `alembic upgrade head` to create the database tables
- to run the project tests `pip install interrobench[dev]` and `python -m pytest` 
- type `interrobench` to run the benchmark

## Database Analysis
There are two tables in the database;
- runs stores general information about the test run and it's results
- attempts stores the logs for the individual attempts and some metadata

### Example queries
If you know SQL you can do some analysis of the results.
```
# find your run
select datetime_start, id from runs;

# see attempts for a given question
select * from attempts where run_id = 13 and function = 'triangle third angle';
```

If you want to see a simple pass/fail result for each question for a
given run, you may notice it's not straightforward to do because we
have a table for individual attempts, not for the overall result after
the best of 5. But you can use this query:
```
SELECT
    function,
    CASE
        WHEN COUNT(CASE WHEN result = 'true' THEN 1 END) >= COUNT(CASE WHEN result != 'true' THEN 1 END)
        THEN true
        ELSE false
    END AS predominant_result
FROM
    attempts
WHERE
    run_id = EDITME
GROUP BY
    function
ORDER BY
    function;
```

### Tidyup
Cascade delete is enabled so if you just delete the run it will clear out the
linked attempts also:
```
delete from runs where id = 13;
```
