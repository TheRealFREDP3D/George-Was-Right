import logging
from typing import Dict

from crewai import Crew, Task
from crewai.tasks.task import Task
from crewai.tasks.task_output import TaskOutput
from crewai.tasks.conditional_task import ConditionalTask

from config import Settings
from agents import AgentFactory, ResearcherAgent, WriterAgent, IllustratorAgent
from tasks import TaskManager
from crewai_tools import SerperDevTool


class CrewBuilder:
    """
    A builder class responsible for constructing and configuring the CrewAI crew.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []

    def initialize_agents(self):
        """
        Initialize and configure agents for the crew.
        """
        agent_factory = AgentFactory(Settings.get_llm())
        search_tool = SerperDevTool(
            n_results=Settings.SEARCH_RESULTS,
            country=Settings.COUNTRY,
            api_key=Settings.SERPER_API_KEY,
        )
        agent_factory.set_search_tool(search_tool)

        self.agents = {
            "researcher": agent_factory.create_researcher_agent(),
            "writer": agent_factory.create_writer_agent(),
            "illustrator": agent_factory.create_illustrator_agent(),
        }

    def create_tasks(self):
        """
        Create tasks for the crew.
        """
        task_manager = TaskManager(self.agents)
        self.tasks = task_manager.create_tasks()

    def build_crew(self) -> Crew:
        """
        Build and return the CrewAI crew.
        """
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True,
            max_rpm=3,
            planning=True,
            planning_llm=Settings.get_llm(),
        )


def main():
    """Main application execution."""
    try:
        # Validate configuration
        Settings.validate()

        # Initialize and build the crew
        crew_builder = CrewBuilder()
        crew_builder.initialize_agents()
        crew_builder.create_tasks()
        crew = crew_builder.build_crew()

        # Execute and log results
        result = crew.kickoff()
        logging.info(f"Analysis completed: {result}")
        print(result)

    except Exception as e:
        logging.error(f"Execution failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
