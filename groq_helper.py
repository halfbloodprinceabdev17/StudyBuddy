import os
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
