"""Part 5: ask for JSON, then check it with Pydantic.  Run: python 05_structured_output.py"""
import json, re
from pydantic import BaseModel
from config import llm
from crewai import Agent, Task, Crew

class PrayerSummary(BaseModel):
    title: str
    prayers: int
    total_fard_rakats: int

def parse_json(text):
    """Models sometimes wrap JSON in ```json fences. Remove them, then parse."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)

agent = Agent(role="Prayer Assistant", goal="Summarise prayer schedules exactly",
              backstory="You are precise with numbers.", llm=llm)

task = Task(
    description=("Summarise this daily prayer schedule: five prayers. "
                 "Fard rakats: Fajr 2, Zuhr 4, Asr 4, Maghrib 3, Isha 4."),
    expected_output=("Reply ONLY with JSON that has exactly these keys: "
                     "title (text), prayers (whole number), total_fard_rakats (whole number)."),
    agent=agent,
)

result = Crew(agents=[agent], tasks=[task]).kickoff()
print("Raw reply:", result.raw)

summary = PrayerSummary(**parse_json(result.raw))     # validation happens here
print(type(summary).__name__, summary)
print("Total fard rakats:", summary.total_fard_rakats)   # expected: 17
print("Checked in code  :", 2 + 4 + 4 + 3 + 4, "->", "OK" if summary.total_fard_rakats == 17 else "MODEL MADE A MISTAKE")
