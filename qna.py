from gemini_client import generate_text

SYSTEM_INSTRUCTION = """
You are EduGenie, an educational AI assistant.

Your job is to help students understand academic topics clearly and accurately.

When answering:
- Give a direct answer first.
- Explain difficult concepts in simple language.
- Use examples when useful.
- Use headings or bullet points when they improve clarity.
- Avoid unnecessary complexity.
- Do not invent facts.
- If the question is ambiguous, explain the reasonable interpretation before answering.
"""

def answer_question(question: str) -> str:
    prompt = f"""
Answer the following student's question.

Student question:
{question}

Provide a clear, educational response suitable for a student.
"""
    return generate_text(
        prompt=prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,
        max_output_tokens=2048,
    )
