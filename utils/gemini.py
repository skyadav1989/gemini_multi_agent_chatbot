import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"
MAX_RETRIES = 3


def gemini_llm(prompt: str) -> str:
    last_exception = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)

            if not response or not response.text:
                raise RuntimeError("Empty response from Gemini")

            return response.text

        except Exception as e:
            last_exception = e
            wait_time = attempt * 1.5  # exponential-ish backoff
            print(f"[Gemini] Attempt {attempt} failed: {e}")
            time.sleep(wait_time)

    # If all retries fail
    raise RuntimeError(
        f"Gemini LLM request failed after {MAX_RETRIES} attempts"
    ) from last_exception
