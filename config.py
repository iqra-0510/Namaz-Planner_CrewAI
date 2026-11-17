"""Shared setup. Every script does:  from config import llm
Reads GROQ_API_KEY from the .env file and builds one LLM object."""
import os, sys, logging
from dotenv import load_dotenv

load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"          # no telemetry
os.environ["CREWAI_TRACING_ENABLED"] = "false"    # no "view tracing?" question

# Windows console: allow emoji and symbols like °C
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "paste_your_key_here":
    raise SystemExit("GROQ_API_KEY not found.\nCopy .env.example to .env and paste your Groq key in it.")

from crewai import LLM

# Groq speaks the OpenAI protocol, so we use the "openai/" connector and point it to Groq.
# Groq shut down llama-3.3-70b-versatile on 16 Aug 2026. Default is now openai/gpt-oss-120b.
# To try another model, add  GROQ_MODEL=qwen/qwen3.6-27b  to your .env file.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
llm = LLM(
    model=f"openai/{GROQ_MODEL}",
    base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"),
    api_key=api_key,
    temperature=0.2,
)
logging.getLogger("crewai.llms.base_llm").setLevel(logging.ERROR)   # hide a harmless warning