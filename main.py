import dotenv
from litellm import cache
from rich import print
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Constants
HOW_MANY_RESULTS = 2
COUNTRY = "us"
MAX_RPM = 5
MAX_ITER = 2
LLM_MODEL = "groq/llama-3.1-70b-versatile"

# Initialize the LLM
try:
    llm = LLM(model=LLM_MODEL)
except Exception as e:
    print(f"Error initializing LLM: {e}")
    llm = None

# Initialize the tool for internet searching capabilities
try:
    search_tool = SerperDevTool(n_results=HOW_MANY_RESULTS, country=COUNTRY, result_as_answer=True)
except Exception as e:
    print(f"Error initializing search tool: {e}")
    search_tool = None

# Define the base agent class
class BaseAgent(Agent):
    def __init__(self, role, goal, backstory, allow_delegation, **kwargs):
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            verbose=True,
            llm=llm,
            cache=True,
            max_rpm=MAX_RPM,
            max_iter=MAX_ITER,
            managin
            **kwargs
        )

# Define specific agent classes
class MagazineOwnerAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Manager",
            goal="Publish articles on the topic of George Orwell's book '1984'.",
            backstory="""
            You have a magazine called 'The Orwellian Times' that publishes articles on the topic of George Orwell's book '1984'.
            You are working for the future of the world. You have a deep understanding of the '1984' theme and the impact it has on society.
            """,
            allow_delegation=False,
            tools=[search_tool] if search_tool else [],
            cache=True,
            **kwargs
        )

class WriterAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Writer",
            goal="Analyse the articles selected by the ResearcherAgent and write a short article comparing a recent news event to a theme from '1984'",
            backstory="""
                You are a talented writer with a knack for translating ideas into compelling articles. 
                You have a deep understanding of the '1984' theme and the impact it has on society.
                You have a dark humor, and you know how to use it to convey the essence of the '1984' theme.
                You are known for your ability to create a unique and engaging tone for each article.
                """
            allow_delegation=True,
            tools=[search_tool] if search_tool else [],
            **kwargs
        )

class IllustratorAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Illustrator",
            goal="Create visual concepts based on provided prompts",
            backstory="You are a talented illustrator with a knack for translating ideas into compelling visuals.",
            allow_delegation=False,
            **kwargs
        )

def create_crew():
    if llm is None or search_tool is None:
        print("Cannot create crew: LLM or search tool initialization failed.")
        return None
    
    # Create agents using the specified LLM and search tool
    researcher = ResearcherAgent(tools=[search_tool])
    writer = WriterAgent()
    illustrator = IllustratorAgent()

    # Create tasks
    tasks = [
        Task(
            description="Search for recent real world news that demonstrate how Orwell's book '1984' is still relevant today",
            agent=researcher,
            expected_output="A list of three recent news events that relate to themes in '1984', the reference url and a snippet"
        ),
        Task(
            description="Compare the news events provided by ResearcherAgent with themes from '1984' and select the most relevant match and write a small article (300-500 words) on the subject.",
            agent=writer,
            expected_output="A short article comparing a recent news event to a theme from '1984'",
        ),
        Task(
            description="Create two sets of prompts: one for an illustration of the current news event and another for an illustration of the similar event or theme from '1984'",
            agent=writer,
            expected_output="Two sets of illustration prompts: one for the news event and one for the '1984' theme",
        ),
    ]

    return Crew(
        agents=[researcher, writer, illustrator],
        tasks=tasks,
        verbose=True,
        llm=llm,
        planning=True,
        output_log_file="output_log.md"
    )
    
def main():
    """
    Executes the main workflow: create a crew, execute tasks, and save the output as markdown.
    """
    crew = create_crew()
    if crew is None:
        print("Crew creation failed. Exiting.")
        return
    
    try:
        result = crew.kickoff()
    except Exception as e:
        print(f"Error during crew execution: {e}")
        return

    print(
    f"""
    JOB DONE                           
    Crew execution completed. 
    
    LLM model used: {LLM_MODEL}
    ***************************************************************************
    """)
    print(result)
    
    # Save the result in markdown format
    try:
        os.makedirs("output", exist_ok=True)
        with open(f"output/{LLM_MODEL}.md", "w") as f:
            f.write(str(result))
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
    
    