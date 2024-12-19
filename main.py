import logging
from typing import Dict, List
from crewai import Crew, Agent
from crewai.task import Task
from config import Settings
from agents import AgentFactory
from tasks import TaskManager
from crewai_tools import SerperDevTool


class CrewBuilder:
    """
    A builder class responsible for constructing and configuring the CrewAI crew.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []

    def create_search_tool(self) -> SerperDevTool:
        """
        Create a search tool instance.
        """
        serper_settings = Settings.SERPER_SEARCH_TOOL_SETTINGS
        n_results = serper_settings["n_results"]
        country = serper_settings["country"]
        api_key = serper_settings["api_key"]
        return SerperDevTool(
            n_results=n_results,
            country=country,
            api_key=api_key,
        )

    def initialize_agents(self) -> None:
        """
        Initialize and configure agents for the crew.
        """
        agent_factory = AgentFactory(Settings.get_llm())
        search_tool = self.create_search_tool()
        agent_factory.set_search_tool(search_tool)

        self.agents = {
            "researcher": agent_factory.create_researcher_agent(),
            "writer": agent_factory.create_writer_agent(),
            "illustrator": agent_factory.create_illustrator_agent(),
        }

    def create_tasks(self, task_manager: TaskManager) -> None:
        """
        Create tasks for the crew using the provided task manager.
        """
        self.tasks = task_manager.create_tasks()

    def build_crew(self) -> Crew:
        """
        Build and return the crew instance.
        """
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True,
            max_rpm=Settings.MAX_RPM,
            planning=Settings.PLANNING,
            planning_llm=Settings.get_llm(),
        )


def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def validate_configuration():
    """
    Validate the application configuration.
    """
    try:
        Settings.validate()
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        raise


def build_crew():
    """
    Initialize and build the CrewAI crew.
    """
    crew_builder = CrewBuilder()
    crew_builder.initialize_agents()
    task_manager = TaskManager(crew_builder.agents)
    crew_builder.create_tasks(task_manager)
    return crew_builder.build_crew()


def main():
    """Main application execution."""
    try:
        # Set up logging
        setup_logging()

        # Validate configuration
        validate_configuration()

        # Build the crew
        build_crew()

        # Additional logic can be added here if needed

    except Exception as e:
        logging.error(f"An error occurred during main execution: {e}")


if __name__ == "__main__":
    main()
