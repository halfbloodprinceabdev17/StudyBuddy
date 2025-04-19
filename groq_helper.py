import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_feedback(question, options, user_answer, correct_answer):
    """Generate a humorous and educational AI feedback using Groq's LLM."""

    prompt = f"""
You're a funny, kind, and slightly sarcastic AI tutor.

The user answered this MCQ:

Question: {question}
Options:
A. {options[0]}
B. {options[1]}
C. {options[2]}
D. {options[3]}

User's answer: {user_answer}
Correct answer: {correct_answer}

If the answer is correct, praise them with a joke or emoji.

If wrong, give:
- A fun/funny but kind reaction
- A simple explanation of why it’s wrong
- A relatable analogy or tip to remember next time

Make it educational but entertaining and conversational.
"""

    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",  # Or use gemma2-9b-it depending on what you prefer
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Oops! Something went wrong generating feedback: {e}"


def extract_mcqs_with_llm(text):
    prompt = f"""
You are an expert quiz generator.

From the text below, extract all multiple-choice questions (MCQs). Format them as a **JSON list** like this:

[
  {{
    "question": "What is the capital of France?",
    "options": ["A. Paris", "B. London", "C. Berlin", "D. Madrid"],
    "answer": "A"
  }},
  ...
]

⚠️ Only return **pure valid JSON**, no commentary, markdown, or text outside the list.

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()

        # Ensure it's JSON — fix minor formatting if needed
        json_start = raw.find('[')
        json_end = raw.rfind(']')
        if json_start == -1 or json_end == -1:
            raise ValueError("Invalid JSON format returned by the LLM.")
        
        json_str = raw[json_start:json_end+1]
        return json.loads(json_str)

    except Exception as e:
        print(f"[Groq Error] {e}")
        return [{"question": "⚠️ Failed to extract MCQs", "options": [], "answer": ""}]

