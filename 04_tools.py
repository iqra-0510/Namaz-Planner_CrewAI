"""Part 4: tools. The agent chooses WHEN to call them.  Run: python 04_tools.py
NOTE: prayer times below are SAMPLE (fake) data for learning. Use a trusted app/mosque timetable for real times."""
from config import llm
from crewai import Agent, Task, Crew
from crewai.tools import tool

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

# TASK 3 (student) - DONE: our own tool  tasbeeh_total(rounds, per_round)
@tool("Tasbeeh total")
def tasbeeh_total(rounds: int, per_round: int) -> str:
    """Calculate the total tasbeeh count. Inputs: rounds (whole number), per_round (whole number)."""
    return str(int(rounds) * int(per_round))

print(get_prayer_time.name, "->", get_prayer_time.description)

assistant = Agent(
    role="Prayer Assistant",
    goal="Answer prayer-planning questions using the tools. Never guess data.",
    backstory="You help people plan their day around prayer. You use a tool for prayer times and for every calculation.",
    tools=[get_prayer_time, calculator],     # the allow-list of this agent
    llm=llm, verbose=True,
    max_iter=6,                              # stop a runaway loop
)

task = Task(
    description=("What is the Fajr time in Lahore? And how many fard rakats are in one day "
                 "if Fajr has 2, Zuhr 4, Asr 4, Maghrib 3 and Isha 4?"),
    expected_output="One short answer with the Fajr time and the total fard rakats.",
    agent=assistant,
)

result = Crew(agents=[assistant], tasks=[task], verbose=True).kickoff()
print("\nANSWER:", result.raw)      # expected total: 17

# ---- TASK 3: agent that uses our own tool ----
counter = Agent(role="Tasbeeh Counter", goal="Count the total exactly using the tool. Never guess.",
                backstory="You always use the Tasbeeh total tool.", tools=[tasbeeh_total], llm=llm, max_iter=5)
count_task = Task(description="I recite tasbeeh 33 times in each of 3 rounds. How many times in total?",
                  expected_output="The total number, as one short sentence.", agent=counter)
print("\nTASK 3 ANSWER:", Crew(agents=[counter], tasks=[count_task]).kickoff().raw)      # expected: 99
