import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

USE_LOCAL_EXPLANATION_MODEL = (
    os.getenv("USE_LOCAL_EXPLANATION_MODEL", "false").lower() == "true"
)

LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M",
)

MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "20000"))
