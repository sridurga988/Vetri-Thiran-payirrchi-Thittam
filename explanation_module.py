from functools import lru_cache

from config import LOCAL_EXPLANATION_MODEL, USE_LOCAL_EXPLANATION_MODEL
from gemini_client import generate_text

@lru_cache(maxsize=1)
def get_local_pipeline():
    if not USE_LOCAL_EXPLANATION_MODEL:
        return None
    try:
        from transformers import pipeline
        return pipeline("text2text-generation", model=LOCAL_EXPLANATION_MODEL)
    except Exception:
        return None

def explain_with_local_model(concept: str, level: str) -> str | None:
    generator = get_local_pipeline()
    if generator is None:
        return None

    prompt = f"""
Explain the following concept for a {level} learner.

Concept:
{concept}

Use simple language and a short example.
"""
    try:
        result = generator(prompt, max_new_tokens=300)
        if result:
            return result[0]["generated_text"].strip()
    except Exception:
        return None
    return None

def explain_concept(concept: str, level: str = "beginner") -> str:
    if USE_LOCAL_EXPLANATION_MODEL:
        local_result = explain_with_local_model(concept, level)
        if local_result:
            return local_result

    prompt = f"""
Explain the concept below to a {level} learner.

Concept:
{concept}

Structure the explanation as:
1. Simple definition
2. How it works
3. Easy example
4. Important points

Keep the explanation student-friendly.
"""
    return generate_text(
        prompt=prompt,
        system_instruction="You are an expert educational tutor who explains concepts simply.",
        temperature=0.4,
        max_output_tokens=2048,
    )
