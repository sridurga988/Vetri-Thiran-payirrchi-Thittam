from gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational content.

Content:
{text}

Requirements:
- Identify the main ideas.
- Remove unnecessary repetition.
- Keep important facts.
- Use simple language.
- Use bullet points where helpful.
- Make the summary easy for a student to revise.
"""
    return generate_text(
        prompt=prompt,
        system_instruction="You are an educational summarization assistant.",
        temperature=0.3,
        max_output_tokens=2048,
    )
