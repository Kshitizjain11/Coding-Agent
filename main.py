from dotenv import load_dotenv

load_dotenv()
from google import genai
import sys
from openai import OpenAI
import os
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content 
from functions.run_python import schema_run_python_file 
from functions.write_file import schema_write_file  
from call_function import call_function

def main():
    client = genai.Client()

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of a file
- Write to a file (create or update)
- Run a Python file with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(2)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    # client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=os.environ['GROQ_API_KEY'])

    # res = client.responses.create(
    #     input=messages,
    #     model="openai/gpt-oss-20b",

    # )
    # print(res.output_text)

    # USing Groq instead of gemini
    res = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages, config=config
    )
    if verbose_flag:
        print("User prompt:", prompt)
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)

    if res.function_calls:
        for function_call in res.function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call,verbose_flag)
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(res.text)
    # print("Prompt tokens:",res.usage.input_tokens)
    # print("Response tokens:" ,res.usage.output_tokens)


if __name__ == "__main__":
    main()
