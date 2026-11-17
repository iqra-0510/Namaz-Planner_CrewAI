"""LAB (student) - DONE: daily ibadah-planner crew.  Run: python 07_lab_ibadah_planner.py
NOTE: prayer times are SAMPLE (fake) data for learning only.

Goal: 3 agents (Prayer Time Planner, Routine Writer, Routine Reviewer), sequential.
Test input: {"city": "Lahore", "work_hours": 8, "quran_minutes": 20, "walk_minutes": 30}
"""
import json, re
from pydantic import BaseModel
from config import llm
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- step 1: tools with fake data
@tool("Get prayer time")
def get_prayer_time(city: str, prayer: str) -> str:
    """Get the SAMPLE time of one prayer in a city. Inputs: city name, prayer name (Fajr, Zuhr, Asr, Maghrib or Isha)."""
    data = {
        "lahore":    {"fajr": "5:40 AM", "zuhr": "12:10 PM", "asr": "3:20 PM", "maghrib": "5:05 PM", "isha": "6:30 PM"},
        "karachi":   {"fajr": "5:55 AM", "zuhr": "12:25 PM", "asr": "3:35 PM", "maghrib": "5:30 PM", "isha": "6:50 PM"},
        "islamabad": {"fajr": "5:45 AM", "zuhr": "12:05 PM", "asr": "3:15 PM", "maghrib": "5:00 PM", "isha": "6:25 PM"},
    }
    aliases = {"dhuhr": "zuhr", "duhr": "zuhr", "zohar": "zuhr", "fajar": "fajr", "magrib": "maghrib", "esha": "isha"}
    times = data.get(city.strip().lower())
    if not times:
        return "no data for this city (available: Lahore, Karachi, Islamabad)"
    name = prayer.strip().lower()
    name = aliases.get(name, name)
    if name not in times:
        return "unknown prayer name (use Fajr, Zuhr, Asr, Maghrib or Isha)"
    return f"{city} {prayer}: {times[name]} (sample data)"

@tool("Time gap")
def time_gap(start: str, end: str) -> str:
    """Minutes between two clock times on the same day. Inputs: start and end like '12:10 PM' and '3:20 PM'."""
    def to_min(t):
        clock, ampm = t.strip().upper().split()
        h, m = (int(x) for x in clock.split(":"))
        if ampm == "PM" and h != 12:
            h += 12
        if ampm == "AM" and h == 12:
            h = 0
        return h * 60 + m
    try:
        gap = to_min(end) - to_min(start)
    except Exception:
        return "ERROR: write times like '5:40 AM'"
    return f"{gap} minutes" if gap >= 0 else "ERROR: end time is before start time"

@tool("Calculator")
def calculator(expression: str) -> str:
    """Calculate a simple maths expression like '17 * 23'. Input: the expression."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "ERROR: only numbers and + - * / ( ) are allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "ERROR: invalid expression"

# --- step 2: agents
time_planner = Agent(
    role="Prayer Time Planner",
    goal="Find the five prayer times of the city and calculate the free time between them",
    backstory=("You are an organised planner. You use the tool for every prayer time, the Time gap tool for "
               "gaps between times and the calculator for every calculation. You never guess."),
    tools=[get_prayer_time, time_gap, calculator], llm=llm, max_iter=12, allow_delegation=False)
routine_writer = Agent(
    role="Routine Writer",
    goal="Write a calm day plan around the prayer times that includes work, Quran reading and a walk",
    backstory="You write short, practical daily plans in simple English. You never change the prayer times.",
    llm=llm, allow_delegation=False)
routine_reviewer = Agent(
    role="Routine Reviewer",
    goal="Check that the plan has all five prayers and fits the day",
    backstory=("You are strict. You check all five prayers are in the plan, work hours are enough and Quran and "
               "walk time are included. You reply APPROVED, or a short list of fixes."),
    llm=llm, allow_delegation=False)

# --- step 3: tasks (placeholders are filled in kickoff)
time_task = Task(
    description=("Get the times of Fajr, Zuhr, Asr, Maghrib and Isha in {city} with the tool. "
                 "Then show the five times in a short table."),
    expected_output="A short table with the five prayer times of {city}.",
    agent=time_planner)
routine_task = Task(
    description=("Write a day plan for a person in {city} who works {work_hours} hours, reads Quran {quran_minutes} minutes "
                 "and walks {walk_minutes} minutes. Put every item around the prayer times from the table."),
    expected_output="A time-by-time plan with all five prayers, work, Quran and walk.",
    agent=routine_writer, context=[time_task])
review_routine_task = Task(
    description=("Review the plan: all five prayers, {work_hours} work hours, {quran_minutes} Quran minutes, "
                 "{walk_minutes} walk minutes. Reply APPROVED, or list what to fix."),
    expected_output="APPROVED, or a short list of fixes.",
    agent=routine_reviewer, context=[time_task, routine_task])

# --- step 4 and 5: crew and test goal
ibadah_crew = Crew(agents=[time_planner, routine_writer, routine_reviewer],
                   tasks=[time_task, routine_task, review_routine_task],
                   process=Process.sequential, verbose=False)

inputs = {"city": "Lahore", "work_hours": 8, "quran_minutes": 20, "walk_minutes": 30}
result = ibadah_crew.kickoff(inputs=inputs)
print("\n=== LAB: FINAL OUTPUT (reviewer) ===\n" + result.raw)
for out in result.tasks_output:
    print("\n--- ", out.agent, "---\n", out.raw[:300])

# --- bonus: JSON + Pydantic check of the minutes, and token usage
class MinutesCheck(BaseModel):
    total_extra_minutes: int
    more_than_one_hour: bool

def parse_json(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)

json_task = Task(
    description=("Add Quran {quran_minutes} minutes and walk {walk_minutes} minutes. "
                 "Work out the total extra minutes and say if it is more than 60."),
    expected_output=("Reply ONLY with JSON that has exactly these keys: "
                     "total_extra_minutes (whole number), more_than_one_hour (true or false)."),
    agent=time_planner)
check = Crew(agents=[time_planner], tasks=[json_task]).kickoff(inputs=inputs)
data = MinutesCheck(**parse_json(check.raw))
expected = inputs["quran_minutes"] + inputs["walk_minutes"]
print("\nBONUS:", data, "| checked in code:", expected, expected > 60)   # expected total: 50, False
print("Token usage of the main run:", result.token_usage)
