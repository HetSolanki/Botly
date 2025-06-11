import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    if not args:
        print("Bolty - (AI Agent)")
        print("\nUsage: python3 main.py <prompt> [--verbose]")
        print("Example: python3 main.py 'How do i build todo-list app in react?'")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    generate_content(client, messages, verbose, system_prompt)


def generate_content(client, messages, verbose, system_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:", response.text)

if __name__ == "__main__":
    main()
