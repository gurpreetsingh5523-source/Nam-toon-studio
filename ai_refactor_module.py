"""
ai_refactor_module.py
LLM-powered code refactoring for Nam-toon-studio. Secure API key handling included.
"""
import os
import openai

def get_openai_api_key():
    # Securely load API key from environment or config
    return os.getenv("OPENAI_API_KEY")

def refactor_code(code_snippet, instruction):
    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError("OpenAI API key not found. Set OPENAI_API_KEY in environment.")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a code refactoring assistant."},
            {"role": "user", "content": f"Refactor this code: {code_snippet}\nInstruction: {instruction}"}
        ]
    )
    return response.choices[0].message['content']

if __name__ == "__main__":
    # Example usage
    code = "def foo():\n    pass"
    print(refactor_code(code, "Remove unused function."))
