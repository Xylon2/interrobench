from pprint import pprint
from shared import prompt_continue, indented_print

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

class NoToolException(Exception):
    """Custom exception for user aborting the operation."""
    pass

class MsgLimitException(Exception):
    """Custom exception for user aborting the operation."""
    pass

initial_messages = [
    SystemMessage(content="""You are a competent and alert chatbot.

You are provided with a mystery function which you will \"interrogate\" to try to determine what it does. Use the provided tool to do this.

At the same time you will tell the user what you are doing.

Once you are confident you know what the function does, you will inform the user.
"""),
    HumanMessage(content="""Hi. I have a mystery function and I want to find out what it does.

I would like you to test my function using the provided tool until you think you know what it does, then tell me."""),
]

def print_tool_call(tool_call, result):
    indented_print(", ".join(map(str, tool_call["args"].values())), "→", result.content)

def interrogate(config, llm, mystery_fn, msgfmt):
    msg_limit = config["msg-limit"]
    debug = config["debug"]

    fn_fn = mystery_fn["function"]

    tool_call_count = 0

    messages = list(initial_messages)  # python by default would just alias the
                                       # new variable to the old one so we use
                                       # list() to force a copy

    for count in range(0, msg_limit):
        # send the chat
        llmout = llm.invoke(messages)

        # append for convo history
        messages.append(llmout)  # it's an AIMessage object

        llm_msg = llmout.content
        tool_calls = llmout.tool_calls  # list of dicts

        print("\n--- LLM ---")
        indented_print(msgfmt(llm_msg))
        
        # if it called the tool
        if tool_calls:
            print("\n### SYSTEM: calling tool")
            for tool_call in tool_calls:
                call_result = fn_fn.invoke(tool_call)

                print_tool_call(tool_call, call_result)
                
                messages.append(call_result)

                tool_call_count += 1

            prompt_continue(config, "prompt-each-message")

        # LLM didn't call the tool, so it's time to run the verifications
        else:
            if tool_call_count == 0:
                raise NoToolException("LLM didn't use it's tool.")
            
            print("\n### SYSTEM: The tool was used", tool_call_count, "times.")

            return(messages)

    # LLM ran out of messages
    raise MsgLimitException("LLM ran out of messages.")
