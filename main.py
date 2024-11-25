from datetime import datetime
from typing import List
import dotenv
import os
from rich import print

from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# import agentops
# agentops.init()


class Config:
    """Central configuration for the application."""

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.search_results = os.getenv("SEARCH_RESULTS", "2")
        self.country = os.getenv("COUNTRY", "us")
        self.llm_model = os.getenv("LLM_MODEL", "ollama/qwen2.5:1.5b")


class AgentFactory:
    """Factory class for creating specialized agents."""

    def __init__(self, llm: LLM, search_tool: SerperDevTool):
        """Initializes the AgentFactory with an LLM and a search tool.

        Args:
            llm (LLM): The LLM to use for generating code.
            search_tool (SerperDevTool): The search tool to use for searching code snippets.
        """
        self.llm = llm
        self.search_tool = search_tool

    def _get_base_agent_config(self) -> dict:
        """Returns the base configuration for all agents."""
        return {
            "verbose": True,
            "cache": True,
            "llm": self.llm,
        }

    def create_researcher_agent(self) -> Agent:
        """Creates a modern surveillance and social control analyst agent."""
        return Agent(
            role="Researcher",
            goal="Provide information to other agents to complete their tasks",
            backstory="Investigative researcher specializing in digital surveillance, "
            "privacy rights, and information control in modern society. "
            "You have a deep passion for Orwell's book, '1984'. ",
            allow_delegation=False,
            tools=[self.search_tool],
            **self._get_base_agent_config(),
        )

    def create_writer_agent(self) -> Agent:
        """Creates a comparative analysis journalist agent."""
        return Agent(
            role="Comparative Analysis Journalist",
            goal="Craft compelling narratives connecting '1984' to current reality",
            backstory="Award-winning journalist skilled in connecting literary analysis "
            "with current events.",
            allow_delegation=True,
            tools=[self.search_tool],
            **self._get_base_agent_config(),
        )

    def create_illustrator_agent(self) -> Agent:
        """Creates a conceptual visual storyteller agent."""
        return Agent(
            role="Conceptual Visual Storyteller",
            goal="Create visual prompts connecting modern surveillance to '1984'",
            backstory="Renowned conceptual artist specializing in visual metaphors "
            "of surveillance and social control.",
            allow_delegation=False,
            tools=[],
            **self._get_base_agent_config(),
        )


class TaskManager:
    """Manages the creation and organization of tasks."""

    def __init__(self, agents: dict):
        self.agents = agents

    def create_tasks(self) -> List[Task]:
        """Creates a list of tasks for the crew to execute."""
        return [
            Task(
                description="""Research and analyze current (2024) global surveillance practices, digital privacy concerns, 
                and social control mechanisms. Focus on:
                1. Government surveillance programs and data collection
                2. Social media monitoring and censorship
                3. Digital privacy breaches and corporate data harvesting
                4. State-sponsored misinformation campaigns
                Provide specific examples with verifiable sources and URLs.""",
                agent=self.agents["researcher"],
                expected_output="Detailed report of 3-5 recent cases with source URLs and key parallels to '1984' themes",
            ),
            Task(
                description="""Write a compelling 700-1000 word analysis that:
                1. Introduces the concept of modern surveillance and control
                2. Presents the researched examples and their implications
                3. Draws specific parallels to Orwell's '1984' predictions
                4. Discusses the societal impact and potential future implications
                5. Concludes with recommendations for maintaining individual privacy and freedom""",
                agent=self.agents["writer"],
                expected_output="Well-structured article with clear sections, supporting evidence, and thought-provoking analysis",
            ),
            Task(
                description="""Create two sets of detailed illustration prompts:
                1. For the modern surveillance scenario:
                   - Depict current digital surveillance methods
                   - Emphasize the ubiquity of monitoring in everyday life
                   - Include elements of social media and data collection
                
                2. For the '1984' parallel:
                   - Reference specific elements from Orwell's novel
                   - Show the similarities with modern surveillance
                   - Incorporate symbolic elements that bridge past and present""",
                agent=self.agents["illustrator"],
                expected_output="Two detailed, contrasting illustration prompts that effectively visualize the comparison",
            ),
        ]


def main():
    """Main execution flow."""
    try:
        # Initialize core components
        config = Config()
        llm = LLM(model=config.llm_model)
        search_tool = SerperDevTool(
            n_results=config.search_results, country=config.country
        )
        agent_factory = AgentFactory(llm, search_tool)

        # Create agents
        agents = {
            "researcher": agent_factory.create_researcher_agent(),
            "writer": agent_factory.create_writer_agent(),
            "illustrator": agent_factory.create_illustrator_agent(),
        }

        # Create and execute crew
        task_manager = TaskManager(agents)
        tasks = task_manager.create_tasks()
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True,
            llm=config.llm_model,
            planning=True,
            planning_llm=config.llm_model,
        )

        # Execute crew and save results
        result = crew.kickoff()
        print(f"""Analysis completed successfully using {config.llm_model}

        ***************************************************************************

        {result}

        ***************************************************************************
        """)
    except Exception as e:
        print(f"An error occurred while executing the crew: {str(e)}")


if __name__ == "__main__":
    main()
