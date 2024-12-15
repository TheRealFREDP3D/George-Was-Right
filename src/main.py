import logging
from typing import Dict

from crewai import Crew

from config import Settings
from agents import AgentFactory
from tasks import TaskManager
from crewai_tools import SerperDevTool


def initialize_agents(agent_factory: AgentFactory, search_tool: SerperDevTool) -> Dict:
    """
    Initialize and configure agents for the crew.

    Args:
        agent_factory (AgentFactory): Agent creation factory
        search_tool (SerperDevTool): Web search tool

    Returns:
        Dictionary of initialized agents
    """
    agent_factory.set_search_tool(search_tool)

    return {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }


def main():
    """Main application execution."""
    try:
        # Validate configuration
        Settings.validate()

        # Initialize components
        llm = Settings.get_llm()
        search_tool = SerperDevTool(
            n_results=Settings.SEARCH_RESULTS,
            country=Settings.COUNTRY,
            api_key=Settings.SERPER_API_KEY,
        )

        # Create agents
        agent_factory = AgentFactory(llm)
        agents = initialize_agents(agent_factory, search_tool)

        # Create and execute crew
        task_manager = TaskManager(agents)
        crew = Crew(
            agents=list(agents.values()),
            tasks=task_manager.create_tasks(),
            verbose=True,
            max_rpm=3,
            planning=True,
            planning_llm=llm,
        )

        # Execute and log results
        result = crew.kickoff()
        logging.info(f"Analysis completed: {result}")
        print(result)

    except Exception as e:
        logging.error(f"Execution failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()
