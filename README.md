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
- an account and API key for whichever LLM provider you want to use
- a computer to install python and postgres on. postgres is how it stores analytics for each run

First checkout this code.

Install these:
- postgresql-server and client
- python3, pip and virtualenv

Create a postgresql database and user.

Create a couple of config files:

A `resources/config.yaml` should look like this (uncomment sections as appropriate):
```
---

msg-limit: 30
best-of: 5
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
#  - easy-tests-only
#  - hard-tests-only

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
- use pip to install the deps from `requirements.txt`
- install interrobench into your virtualenv with `pip install -e .`
- set variable DATABASE_URL for alembic and run `alembic upgrade head`
- type `pytest` to run tests
- type `interrobench` to run the benchmark
