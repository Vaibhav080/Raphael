import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini api key environment variable not set.")

client = genai.Client(api_key = API_KEY)

MODEL_NAME = "gemini-3.6-flash"

def generate_response(prompt: str) -> str:
    '''
    Generate a response using Gemini
    '''
    
    response = client.models.generate_content(model = MODEL_NAME, contents = prompt)
    
    return response.text

def main():
    print("Gemini client initialized.")
    
    prompt = input("\nEnter a prompt for Gemini: ")
    
    response = generate_response(prompt)
    
    print()
    print("=" * 60)
    print("GEMINI RESPONSE")
    print("=" * 60)
    print(response)
    
if __name__ == "__main__":
    main()
    