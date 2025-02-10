import requests
import os
from aineta.utils import load_mailboxes
import time
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

def analyze_with_openai(message, mail_prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = next((mailbox["PROMPT"] for mailbox in load_mailboxes("mailboxes.json") if mailbox["EMAIL_ACCOUNT"] == mail_prompt), "Default prompt if not found")
    
    user_message = str(message).strip() if message else ""
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.8,
        "max_tokens": 2000,
    }

    retry_attempts = 100
    for attempt in range(1, retry_attempts + 1):
        try:
            response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except requests.HTTPError as http_err:
            print(f"Error during OpenAI API call (Attempt {attempt}/{retry_attempts}): {http_err}")
            print("Response text:", response.text)
            time.sleep(2)
        except Exception as err:
            print(f"Unexpected error during OpenAI API call (Attempt {attempt}/{retry_attempts}): {err}")
            time.sleep(2)
    return "Error processing response from OpenAI API."
