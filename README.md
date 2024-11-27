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
rate-limit: 0.3  # requests per second
best-of: 5       # how many times is each function tested
model:
  name: "claude-3-5-haiku-20241022"
  provider: "anthropic"
#model:
#  name: "gpt-4o-mini"
#  provider: "openai"
#model:
#  name: "grok-beta"
#  provider: "xai"
#model:
#  name: "command-r-plus"
#  provider: "cohere"
  
debug:
#  - prompt-each-interrogation
#  - prompt-each-message
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
- type `pytest` to run tests
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

### Tidyup
Cascade delete is enabled so if you just delete the run it will clear out the
linked attempts also:
```
delete from runs where id = 13;
```
