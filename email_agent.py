import os
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import math
import time
import argparse

load_dotenv()


def review_email(email, mode='huggingface'):

    if mode == 'openai':
        hf_api_key = os.getenv("OpenAI_API_KEY")
        client = OpenAI(
            api_key=hf_api_key,
        )
        model = "gpt-4o"
    else:
        hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_api_key,
        )
        model = "openai/gpt-oss-120b:nscale"



    def get_response(client, model, prompt, retries = 5, backoff = 1):
        """Send prompt to the model with retry logic for rate limits."""
        for i in range(retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    #model="openai/gpt-oss-120b:nscale",
                    #model="gpt-4o",  # Switch to GPT-4o
                
                    messages=[
                        {
                        "role": "system",
                        "content": (
                            "You are an Email Review Assistant. Your task is to proofread and improve the professionalism of emails provided by the user. "
                            "Always use British English spelling and grammar. Assume the sender is Anthony Cutajar, a Data Scientist working in Market Research. "
                            "Return only the improved email body (no subject line or commentary). "
                            "If the email has an angry or frustrated tone, respond only with 'Calm Down'.")},
                        {"role": "user", "content": prompt}],
                    temperature=1.2,
                )
                return response.choices[0].message.content
            
            except RateLimitError:
                wait = backoff * (2 ** i)  # exponential backoff
                print(f"Rate limit hit. Waiting {wait:.2f} seconds...")
                time.sleep(wait)

        raise Exception("Failed after retries due to rate limits.")


    prompt = f"""Proofread the following email for grammar and spelling mistakes. Make it concise and professional. Email : {email}"""

    suggestion = get_response(client, model, prompt, retries = 5, backoff = 1)
    print("Orignal Text:", email)
    print("\nSuggestion:  ", suggestion)
    
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Review and improve an email.")
    parser.add_argument("--email", type=str, required=False, help="The email text to be reviewed.")
    parser.add_argument("--mode", type=str, choices=['huggingface', 'openai'], default='huggingface', help="Choose the model provider.")
    args = parser.parse_args()
    #email = "What do you reckon we get for lunch aye?"
    #mode = 'huggingface'  # or 'openai'
    review_email(args.email, args.mode)