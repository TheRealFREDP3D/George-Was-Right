from datetime import datetime
from typing import List
import dotenv
from rich import print

from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool


import agentops

class Config:
    """Central configuration for the application."""
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    SEARCH_RESULTS = 2
    COUNTRY = "us"
    LLM_MODEL = "groq/llama-3.2-90b-text-preview"

# Load environment variables
dotenv.load_dotenv()

# Initialize agentops
agentops.init()

# Initialize the search tool
search_tool = SerperDevTool(
    n_results=Config.SEARCH_RESULTS,
    country=Config.COUNTRY
)

class AgentFactory:
    """Factory class for creating specialized agents."""
    
    def __init__(self, llm: LLM):
        self.llm = llm
        
    def create_researcher_agent(self) -> Agent:
        """Creates a modern surveillance and social control analyst agent."""
        return Agent(
            role="Senior Researcher",
            goal="Provide other agents with the information they ask to complete their tasks",
            backstory="""Investigative researcher specializing in digital surveillance,
            privacy rights, and information control in modern society.""",
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
            cache=True,
            tools=[search_tool]
        )

    def create_writer_agent(self) -> Agent:
        """Creates a comparative analysis journalist agent."""
        return Agent(
            role="Comparative Analysis Journalist",
            goal="Craft compelling narratives connecting '1984' to current reality",
            backstory="""Award-winning journalist skilled in connecting literary analysis
            with current events.""",
            allow_delegation=True,
            verbose=True,
            tools=[], 
            cache=True,
            llm=self.llm
        )

    def create_illustrator_agent(self) -> Agent:
        """Creates a conceptual visual storyteller agent."""
        return Agent(
            role="Conceptual Visual Storyteller",
            goal="Create visual prompts connecting modern surveillance to '1984'",
            backstory="""Renowned conceptual artist specializing in visual metaphors
            of surveillance and social control.""",
            allow_delegation=False,
            verbose=True,
            tools=[],
            cache=True,
            llm=self.llm
        )

class TaskManager:
    """Manages the creation and organization of tasks."""
    
    @staticmethod
    def create_tasks(agents: dict) -> List[Task]:
        """Creates a list of tasks for the crew to execute."""
        return [
            Task(
                description="Search for recent real world news that demonstrate how Orwell's book '1984' is still relevant today.",
                agent=agents['researcher'],
                expected_output="A list of recent relevant world news with source references URLs"
            ),
            Task(
                description="Write comparative analysis article. 700-1000 words.",
                agent=agents['writer'],
                expected_output="Article comparing news event to '1984' theme"
            ),
            Task(
                description="Create illustration prompts for both contexts",
                agent=agents['illustrator'],
                expected_output="Two sets of illustration prompts"
            )
        ]

def main():
    """Main execution flow."""
    # Initialize core components
    llm = LLM(model=Config.LLM_MODEL)
    agent_factory = AgentFactory(llm)

    # Create agents
    agents = {
        'researcher': agent_factory.create_researcher_agent(),
        'writer': agent_factory.create_writer_agent(),
        'illustrator': agent_factory.create_illustrator_agent()
    }

    # Create and execute crew
    tasks = TaskManager.create_tasks(agents)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True,
        llm=Config.LLM_MODEL,
        planning=True, 
        planning_lll=Config.LLM_MODEL
    )

    try:
        # Execute crew and save results
        result = crew.kickoff()
        print(f"""Analysis completed successfully using {Config.LLM_MODEL}

        ***************************************************************************

        {result}

        ***************************************************************************
        """)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
