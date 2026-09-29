from gemini_client import generate_text

def generate_learning_path(
    goal: str,
    level: str = "beginner",
    timeline: str = "4 weeks",
) -> str:
    prompt = f"""
Create a personalized learning path for a student.

Learning goal:
{goal}

Current level:
{level}

Available timeline:
{timeline}

Include:
1. Learning stages
2. Topics to study
3. Weekly or stage-wise timeline
4. Practice activities
5. Small project ideas
6. Revision suggestions
7. Recommended types of learning resources

Make the plan practical and achievable.
Adapt it to the student's current level.
"""
    return generate_text(
        prompt=prompt,
        system_instruction="You are EduGenie, a personalized learning-path assistant.",
        temperature=0.5,
        max_output_tokens=3000,
    )
