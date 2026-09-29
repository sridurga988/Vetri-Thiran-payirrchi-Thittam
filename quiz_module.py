import json
import re

from gemini_client import generate_text

def clean_json_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

def validate_quiz(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Quiz response must be an object.")

    questions = data.get("questions")
    if not isinstance(questions, list):
        raise ValueError("Quiz response must contain a questions list.")

    if len(questions) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be an object.")

        for field in ["question", "options", "answer"]:
            if field not in question:
                raise ValueError(f"Missing quiz field: {field}")

        if not isinstance(question["options"], list):
            raise ValueError("Question options must be a list.")

        if len(question["options"]) != 4:
            raise ValueError("Each question must have exactly 4 options.")

    return data

def generate_quiz(topic: str) -> dict:
    prompt = f"""
Create a multiple-choice quiz about:

{topic}

Return ONLY valid JSON.

The JSON format must be:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Correct option"
    }}
  ]
}}

Requirements:
- Exactly 3 questions.
- Exactly 4 options for every question.
- One correct answer per question.
- Questions should test understanding.
- Do not add explanations outside the JSON.
"""
    response = generate_text(
        prompt=prompt,
        system_instruction="You create accurate educational multiple-choice quizzes.",
        temperature=0.5,
        max_output_tokens=2048,
    )

    cleaned = clean_json_response(response)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid quiz JSON.") from exc

    return validate_quiz(data)
