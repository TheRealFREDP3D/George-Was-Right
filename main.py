"""
A CrewAI-based system for analyzing parallels between Orwell's '1984' and modern events.
This module coordinates multiple AI agents to research, analyze, and create content.
"""

import os
from datetime import datetime
from typing import List

import dotenv
from rich import print
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

class Config:
    """Central configuration for the application."""
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    SEARCH_RESULTS = 2
    COUNTRY = "us"
    LLM_MODEL = "groq/llama3-70b-8192"

# Load environment variables
dotenv.load_dotenv()

class AgentFactory:
    """Factory class for creating specialized agents."""
    
    def __init__(self, llm: LLM):
        self.llm = llm
        self.search_tool = SerperDevTool(
            n_results=Config.SEARCH_RESULTS,
            country=Config.COUNTRY
        )

    def create_researcher_agent(self) -> Agent:
        """Creates a modern surveillance and social control analyst agent."""
        return Agent(
            role="Gathering Information on Internet",
            goal="Provide other agents with the information they ask to complete their tasks",
            backstory="""Investigative researcher specializing in digital surveillance,
            privacy rights, and information control in modern society.""",
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
            cache=True,
            tools=[self.search_tool]
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
            backstory="""
                Renowned conceptual artist specializing in visual metaphors
                of surveillance and social control.
                """,
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
                description="Find recent news showing '1984' relevance today",
                agent=agents['researcher'],
                expected_output="Three recent relevant news events with URLs"
            ),
            Task(
                description="Write comparative analysis article",
                agent=agents['writer'],
                expected_output="Article comparing news event to '1984' theme"
            ),
            Task(
                description="Create illustration prompts for both contexts",
                agent=agents['illustrator'],
                expected_output="Two sets of illustration prompts"
            )
        ]

def save_output(output: str, model: str):
    """Save crew output to file."""
    # Split model string into provider and model_name
    provider, model_name = model.split('/')
    
    # Create output directory if it doesn't exist
    output_dir = f"output/{provider}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp
    filename = f"{output_dir}/{model_name}-{Config.TIMESTAMP}.md"
    
    # Save output to file
    with open(filename, "w") as f:
        f.write(output)
    
    return filename

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
        llm=llm
    )

    # Execute crew and save results
    result = crew.kickoff()
    output_file = save_output(str(result), Config.LLM_MODEL)
    
    print(f"\nAnalysis completed successfully using {Config.LLM_MODEL}")
    print(f"result")
    print(str(output_file))

if __name__ == "__main__":
    main()
