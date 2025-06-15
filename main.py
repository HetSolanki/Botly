import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    load_dotenv()

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    

    if not args:
        print("Bolty - (AI Agent)")
        print("\nUsage: python3 main.py <prompt> [--verbose]")
        print("Example: python3 main.py 'How do i fix calculator'")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.") 
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose, system_prompt)
            if final_response:
                print("Final Response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose, system_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig( 
            tools=[available_functions], system_instruction=system_prompt
        ),
    )  

    if response.candidates:
        messages.append(response.candidates[0].content)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts 
            or not function_call_result.parts[0].function_response.response
        ):
            raise Exception(f"Error While accessing the function response")
    
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

        messages.append(function_call_result)

    if not function_responses:
        raise Exception("no function response genereted, exiting.")
            

if __name__ == "__main__":
    main()
