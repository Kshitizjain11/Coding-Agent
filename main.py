from dotenv import load_dotenv
load_dotenv()
from google import genai
import sys
from openai import OpenAI
import os
from google.genai import types

def main():
    client = genai.Client()
    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(2)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == '--verbose':
        verbose_flag = True

    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]



    # client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=os.environ['GROQ_API_KEY'])

    # res = client.responses.create(
    #     input=messages,
    #     model="openai/gpt-oss-20b",
    # )
    # print(res.output_text)

    #USing Groq instead of gemini
    res = client.models.generate_content(model="gemini-2.5-flash",contents=messages)
    print(res.text)
    if (verbose_flag):
        print("User prompt:",prompt)
        print("Prompt tokens:",res.usage_metadata.prompt_token_count)
        print("Response tokens:" ,res.usage_metadata.candidates_token_count)
    # print("Prompt tokens:",res.usage.input_tokens)
    # print("Response tokens:" ,res.usage.output_tokens)

if __name__ == "__main__":
    main()
