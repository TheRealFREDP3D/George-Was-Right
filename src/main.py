import logging
from typing import Dict, List
from crewai import Crew, Task, Agent, LLM
from config import Settings
from agents import AgentFactory
from tasks import TaskManager
from crewai_tools import SerperDevTool
from rich import print


class CrewBuilder:
    """A builder class responsible for constructing and configuring the CrewAI crew."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Task] = []

    def _initialize_agents(self) -> None:
        """Initialize and configure agents for the crew."""
        agent_factory = AgentFactory(Settings.get_llm())
        search_tool = SerperDevTool(
            n_results=Settings.SERPER_SEARCH_TOOL_SETTINGS["n_results"],
            country=Settings.SERPER_SEARCH_TOOL_SETTINGS["country"],
            api_key=Settings.SERPER_SEARCH_TOOL_SETTINGS["api_key"],
        )

        agent_factory.set_search_tool(search_tool)
        self.agents = {
            "researcher": agent_factory.create_researcher_agent(),
            "writer": agent_factory.create_writer_agent(),
            "illustrator": agent_factory.create_illustrator_agent(),
        }

    def _create_tasks(self) -> None:
        """Create tasks for the crew."""
        task_manager = TaskManager(self.agents)
        self.tasks = task_manager.create_tasks()

    def build_crew(self) -> Crew:
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


def main() -> None:
    """Main application execution."""
    try:
        # Validate configuration
        Settings.validate()
        # Initialize and build the crew
        crew = CrewBuilder().build_crew()
        # Execute and log results
        result = crew.kickoff()
        logging.info(f"Analysis completed: {result}")
        print(result)
    except Exception as e:
        logging.error(f"Execution failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
