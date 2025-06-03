from ai_agent_functions import Functions
from ai_agent_tools import (
    get_stock_live_data_tool,
    get_stock_additional_info_tool,
    get_companies_by_result_date_tool,
)
import sys
import asyncio
import os
import torch
import json
from together import Together

# Fix for Torch on Windows
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# LLM Configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "89f13a053f68784660edf1ac4fc8c2e3cfd83092338883bf0009f46e9408dff3")
together_client = Together(api_key=TOGETHER_API_KEY)
LLM_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
system_message = {
    "role": "system",
    "content": '''
You are an AI stock analyst chatbot that answers financial queries using tool-based functions only.'''
}

# Call the LLM
def call_llm(messages, tools=None, temperature=0):
    print("\n====== Calling LLM ====")

    response = together_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
        temperature=temperature,
    )
    print("=== LLM Response Received ===")
    return response.choices[0].message

# Map tool names to functions
def process_tool_call(tool):
    print(f"\n--- Processing Tool Call: {tool.function.name} ---")
    available_functions = {
        'get_stock_live_data': Functions.get_stock_live_data,
        'get_stock_additional_info': Functions.get_stock_additional_info,
        'get_companies_by_result_date': Functions.get_companies_by_result_date
    }

# try:
    function_to_call = available_functions[tool.function.name]
    args = json.loads(tool.function.arguments)
    print(f"Arguments: {args}")
    result = function_to_call(**args)
    print("Tool call result received")

    if isinstance(result, list):
        result = "\n".join(f"- {item}" for item in result)
    print(f"Result (first 100 chars): {result[:100]}")
    return {
        "role": "tool",
        "tool_call_id": tool.id,
        "name": tool.function.name,
        "content": f"TOOL RESPONSE ({tool.function.name}):\n{result}"
    }
    # except Exception as e:
    #     print(f"Tool {tool.function.name} failed: {str(e)}")
    #     return {
    #         "role": "tool",
    #         "tool_call_id": tool.id,
    #         "name": tool.function.name,
    #         "content": f"TOOL ERROR: {str(e)}"
    #     }

# Core chatbot function
def tool_calling(query, memory=None):
    print("\n=== Starting Tool Calling ===")
    print(f"User query: {query}")
    messages = memory[:] if memory else []
    messages.append(system_message)
    messages.append({'role': 'user', 'content': query})

    # Initial LLM response with potential tool calls
    print("Calling LLM for initial response----")
    response = call_llm(
        messages,
        tools=[
            get_stock_live_data_tool,
            get_stock_additional_info_tool,
            get_companies_by_result_date_tool
        ],
        temperature=0
    )
    messages.append(response)

    # Process tools if tool calls are present
    if getattr(response, 'tool_calls', None):
        print(f"Tool calls detected: {len(response.tool_calls)}")
        tool_responses = []
        for tool_call in response.tool_calls:
            print(f"Processing tool: {tool_call.function.name}")
            tool_responses.append(process_tool_call(tool_call))
        messages.extend(tool_responses)

        print("Calling LLM with tool responses...")
        final_response = call_llm(messages, temperature=0)
        print("Final response received")
        print(f"Final content (first 100 chars): {final_response.content}")
        return final_response.content

    print("No tool calls detected; returning initial response.")
    return response.content
