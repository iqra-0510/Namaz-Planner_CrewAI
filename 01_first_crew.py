"""Part 1: one agent, one task, one crew.  Run: python 01_first_crew.py"""
from config import llm
from crewai import Agent, Task, Crew

guide = Agent(
    role="Namaz Guide",
    goal="Explain simple daily-prayer ideas so that a beginner understands them",
    backstory="You help young Muslims build a calm prayer habit. You use simple words, short lines and a kind tone.",
    llm=llm,
    verbose=True,
)

explain_task = Task(
    description="Explain {topic} in 3 short lines, with one tiny practical tip.",
    expected_output="3 short lines and one tip.",
    agent=guide,
)

crew = Crew(agents=[guide], tasks=[explain_task], verbose=True)

result = crew.kickoff(inputs={"topic": "why we pray five times a day"})   # normal kickoff() is correct in a script

print("\n", type(result).__name__)
print(result.raw)
