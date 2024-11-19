# InterroBench
[![Python application](https://github.com/Xylon2/interrobench/actions/workflows/python-app.yml/badge.svg)](https://github.com/Xylon2/interrobench/actions/workflows/python-app.yml)

## Intro

A benchmark for LLMs

Each test will be a conversation where the AI has to interrogate a "black box"
function to find out what the function does.

i.e. each time the LLM will propose a set of inputs to test the function, and
then it will receive the output in the response.

When the LLM is confident it has figured it out, then the system tests the LLM
got it right by asking it what output it would expect the function to provide
from a given input.

If you want to see the results: see [The LeaderBoard](https://interrobench.com/).

## Running

If you want to run this benchmark yourself, you will need to create a couple of config files:

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

And a `resources/credentials.yaml` containing your API keys:
```
---

api-keys:
  anthropic: ""
  openai: ""
  xai: ""
  cohere: ""

```

Running it should be essentially:
- ensure you have python3, pip and virtualenv installed
- make a virtualenv
- use pip to install the deps from `requirements.txt`
- install interrobench into your virtualenv with `pip install -e .`
- type `pytest` to run tests
- type `interrobench` to run the benchmark
