"""Part 2: same task, different backstory -> different style.  Run: python 02_role_goal_backstory.py"""
from config import llm
from crewai import Agent, Task, Crew

TOPIC = "keeping focus (khushu) in prayer"

def ask(role, goal, backstory):
    agent = Agent(role=role, goal=goal, backstory=backstory, llm=llm)
    task = Task(description="Explain {topic} in 3 short lines, with one tiny practical tip.",
                expected_output="3 short lines and one tip.", agent=agent)
    return Crew(agents=[agent], tasks=[task]).kickoff(inputs={"topic": TOPIC}).raw

print("=== GENTLE ===")
print(ask("Gentle Guide", "Make the person feel calm and encouraged",
          "You are a kind and patient teacher. You speak softly and encourage small steps."))

print("\n=== BRIEF ===")
print(ask("Brief Reminder Bot", "Give very short and clear reminders",
          "You write short bullet-style reminders. You never use jokes and never write long text."))

# TASK 1 (student) - DONE: a THIRD agent with a very different personality (a cricket lover).
print("\n=== CRICKET LOVER ===")
print(ask("Cricket-Loving Prayer Guide",
          "Explain prayer-habit ideas with a cricket example that makes beginners smile",
          "You are a friendly teacher who loves cricket. You joke a little, stay respectful about prayer, "
          "and always use one cricket example (like keeping your eyes on the ball)."))

# ANSWER: the BACKSTORY changed the style the most (tone, jokes, cricket example).
# Role and goal say WHAT the agent is and wants; the backstory tells it HOW to behave and speak.
