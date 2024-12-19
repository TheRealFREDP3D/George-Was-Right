import logging
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from crewai import Crew, Agent
from crewai.task import Task  # Updated import statement
from .config import Settings  # Modified import statement to be relative
from .agents import AgentFactory
from .tasks import TaskManager
from crewai_tools import SerperDevTool


class CrewBuilder:
    """
    A builder class responsible for constructing and configuring the CrewAI crew.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []

      def _create_search_tool(self) -> SerperDevTool -> None:
        """Create a search tool instance."""
        return SerperDevTool(
            n_results=Settings.SERPER_SEARCH_TOOL_SETTINGS["n_results"],
            country=Settings.SERPER_SEARCH_TOOL_SETTINGS["country"],
            api_key=Settings.SERPER_SEARCH_TOOL_SETTINGS["api_key"],
        )
    
    def initialize_agents(self) -> None:
        """
        Initialize and configure agents for the crew.
        """
        search_tool: SerperDevTool = self.create_search_tool()
        agent_factory: AgentFactory = AgentFactory(Settings.get_llm())

    def create_search_tool(self) -> SerperDevTool:
        """
        Create a search tool instance.
        """
        return SerperDevTool(
            n_results=Settings.SEARCH_RESULTS,
            country=Settings.COUNTRY,
            api_key=Settings.SERPER_API_KEY,
        )
    
    def initialize_agents(self) -> None:
        """
        Initialize and configure agents for the crew.
        """
        search_tool: SerperDevTool = self.create_search_tool()
        agent_factory: AgentFactory = AgentFactory(Settings.get_llm())
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
    
    def _create_tasks(self, task_manager: TaskManager) -> None -> None:
        """Create tasks for the crew using the provided task manager."""
        self.tasks = task_manager.create_tasks()
        
    def build_crew(self) -> Crew:
        """
        Build and return the crew instance.
        """
        # Complete the implementation and add type hints for the return value
        crew: Crew = Crew(self.agents, self.tasks)
        return crew


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
    crew_builder.create_tasks()
    return crew_builder.build_crew()
        """Build and return the CrewAI crew."""
        self._initialize_agents()
        self._create_tasks()
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True,
            # max_rpm=3,
            planning=True,
            planning_llm=Settings.get_llm(),
        )
        """
        Build and return the crew instance.
        """
        # Complete the implementation and add type hints for the return value
        crew: Crew = Crew(self.agents, self.tasks)
        return crew


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
    crew_builder.create_tasks()
    return crew_builder.build_crew()
        """Build and return the CrewAI crew."""
        self._initialize_agents()
        self._create_tasks()
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True,
            # max_rpm=3,
            planning=True,
            planning_llm=Settings.get_llm(),
        )
        """
        Build and return the crew instance.
        """
        # Complete the implementation and add type hints for the return value
        crew: Crew = Crew(self.agents, self.tasks)
        return crew


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
    crew_builder.create_tasks()
    return crew_builder.build_crew()


def main():
    """Main application execution."""
    try:
        # Set up logging
        setup_logging()

        # Set up logging
        setup_logging()

        # Validate configuration
        Settings.validate()
        # Initialize and build the crew
        crew = CrewBuilder().build_crew()
        # Execute and log results
        result = crew.kickoff()
        logging.info(f"Analysis completed: {result}")
        print(result)
        validate_configuration()

        # Build the crew
        build_crew()

        # Additional logic can be added here if needed

    except Exception as e:
        logging.error(f"An error occurred during main execution: {e}")
        logging.error(f"An error occurred during main execution: {e}")


if __name__ == "__main__":
    main()
