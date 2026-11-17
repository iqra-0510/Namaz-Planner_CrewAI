"""Part 3: agents work one after another (sequential).  Run: python 03_team_sequential.py"""
from config import llm
from crewai import Agent, Task, Crew, Process

researcher = Agent(role="Researcher", goal="Find the key points about a calm-living habit",
                   backstory="You are careful. You give only points you are sure about, as short bullets. You avoid religious rulings.", llm=llm)
writer = Agent(role="Writer", goal="Turn notes into a clear short text for beginners",
               backstory="You write simple English. You never add points that are not in the notes.", llm=llm)
# TASK 2 (student) - DONE: third agent "Reviewer"
reviewer = Agent(role="Reviewer", goal="Check a text and approve it or list fixes",
                 backstory="You are strict but fair. You check the text is about 80 words, simple, and has no religious rulings. "
                           "You reply APPROVED, or a short list of fixes.", llm=llm)

research_task = Task(description="Collect 4 key points about {topic}.", expected_output="4 bullet points.", agent=researcher)
write_task = Task(description="Write a text of about 80 words about {topic} using ONLY the points from the research.",
                  expected_output="One paragraph of about 80 words.", agent=writer,
                  context=[research_task])      # "use the output of research_task"
# TASK 2 (student) - DONE: third task, context=[write_task]
review_task = Task(description="Review the text. Reply APPROVED, or list what to fix.",
                   expected_output="APPROVED, or a short list of fixes.", agent=reviewer,
                   context=[write_task])

team = Crew(agents=[researcher, writer, reviewer], tasks=[research_task, write_task, review_task],
            process=Process.sequential, verbose=True)

result = team.kickoff(inputs={"topic": "a regular daily routine for a peaceful mind"})
print("\n===== FINAL (REVIEWER) =====")
print(result.raw)

print("\n===== EACH TASK =====")
for out in result.tasks_output:
    print("AGENT:", out.agent)
    print(out.raw[:200], "\n")

# NOTE: a crew runs each task once. To loop (writer fixes -> reviewer checks again), write a normal
# Python loop around kickoff() with a maximum number of rounds.
