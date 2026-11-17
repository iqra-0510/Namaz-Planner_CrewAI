"""Part 6: a manager LLM decides who does what.  Run: python 06_hierarchical.py"""
from config import llm
from crewai import Agent, Task, Crew, Process

researcher = Agent(role="Researcher", goal="Find the key points about a topic",
                   backstory="You are careful and give short bullet points. You avoid religious rulings.", llm=llm, allow_delegation=False)
writer = Agent(role="Writer", goal="Write clear short texts for beginners",
               backstory="You write simple, calm English.", llm=llm, allow_delegation=False)

big_task = Task(
    description="Prepare a short beginner text (about 80 words) about {topic}. First get the points, then write the text.",
    expected_output="One paragraph of about 80 words.",
    # no agent here: the manager decides
)

crew = Crew(agents=[researcher, writer], tasks=[big_task],
            process=Process.hierarchical, manager_llm=llm, verbose=True)

result = crew.kickoff(inputs={"topic": "finding peace through regular remembrance of Allah (dhikr)"})
print("\n===== FINAL TEXT =====")
print(result.raw)
print("\nToken usage:", result.token_usage)
