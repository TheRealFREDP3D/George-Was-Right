import dotenv
from rich import print
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# Load environment variables from .env file
dotenv.load_dotenv()

# Constants
HOW_MANY_RESULTS = 2
COUNTRY = "us"
LLM_MODEL = "groq/mixtral-8x7b-32768"

# Initialize the LLM
llm = LLM(model=LLM_MODEL)

# Initialize the tool for internet searching capabilities
search_tool = SerperDevTool(n_results=HOW_MANY_RESULTS, country=COUNTRY)

# Define the agents
class ResearcherAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Researcher",
            goal="Research real world news to find and compare with Orwell's '1984' themes.",
            backstory="You are an expert researcher with a keen eye for current events and literary analysis.",
            allow_delegation=False,
            verbose=True,
            llm=llm,
            **kwargs
        )

class WriterAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Writer",
            goal="Gather examples of real world news events that could be from Orwell's '1984' book",
            backstory="You are a skilled writer with a deep understanding of literature and current affairs.",
            allow_delegation=False,
            verbose=True,
            llm=llm,
            **kwargs
        )

class IllustratorAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Illustrator",
            goal="Create visual concepts based on provided prompts",
            backstory="You are a talented illustrator with a knack for translating ideas into compelling visuals.",
            allow_delegation=True,
            verbose=True,
            llm=llm,
            **kwargs
        )

def create_crew():
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
            description="Compare the news events with themes from '1984' and select the most relevant match and write a small article (300-500 words) on the subject.",
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
        output_log_file="output_log.md"
    )
    
def main():
    """
    Executes the main workflow: create a crew, execute tasks, and save the output as markdown.
    """
    crew = create_crew()
    result = crew.kickoff()

    print(
    f"""
    JOB DONE                           
    Crew execution completed. 
    
    LLM model used: {LLM_MODEL}
    ***************************************************************************
    """)
    print(result)
    
    # Save the result in markdown format
    with open(f"output/{LLM_MODEL}.md", "w") as f:
        f.write(str(result))

if __name__ == "__main__":
    main()