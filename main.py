"""
George Was Right - AI-Powered Analysis of Modern Surveillance Through Orwell's Lens

This script implements a multi-agent system using CrewAI to analyze modern surveillance
and privacy issues through the lens of George Orwell's "1984". The system orchestrates
three specialized AI agents to research, analyze, and create content about parallels
between current events and Orwell's predictions.

The system uses:
- A researcher agent to gather current news and data
- A writer agent to analyze parallels with "1984"
- An illustrator agent to create visual concepts

Dependencies:
    - datetime: Timestamp generation
    - typing: Type hints
    - dotenv: Environment variable management
    - rich: Enhanced terminal output
    - crewai: Agent and crew management
    - crewai_tools: Web search capabilities
"""

import os
import openai
from datetime import datetime
from typing import List, Dict
import dotenv
import os
from rich import print
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# Load environment variables from .env file
dotenv.load_dotenv()

# Global configuration constants
COUNTRY = "us"  # Target country for search results
SEARCH_RESULTS = 1  # Number of search results to retrieve
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Get API key from environment

if not SERPER_API_KEY:
    raise ValueError(
        "SERPER_API_KEY environment variable not found. Please add it to your .env file."
    )

LLM_MODEL = LLM(
  model="hf:mistralai/Mistral-7B-Instruct-v0.3",
  api_key=os.environ.get("GLHF_API_KEY"),
  base_url="https://glhf.chat/api/openai/v1",
)  # LLM model identifier


class Config:
    """Central configuration for the application.

    This class manages global configuration settings including timestamps
    for file naming and output organization.

    Attributes:
        TIMESTAMP (str): Current timestamp in YYYY-MM-DD-HH-MM-SS format
        llm_model (str): LLM model identifier
        country (str): Target country for search results
        search_results (int): Number of search results to retrieve
    """

    TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    llm_model = LLM_MODEL
    country = COUNTRY
    search_results = SEARCH_RESULTS


# Initialize the search tool with configured parameters
search_tool = SerperDevTool(
    n_results=SEARCH_RESULTS, country=COUNTRY, api_key=SERPER_API_KEY
)


class AgentFactory:
    """Factory for creating specialized agents."""

    def __init__(self, llm: LLM, tool_callback=None):
        """Initialize the factory with a language model.

        Args:
            llm (LLM): Language model instance for agent operations
            tool_callback (callable, optional): Callback function for tool outputs
        """
        self.llm = llm
        self.tool_callback = tool_callback
        self.search_tool = None

    def set_search_tool(self, search_tool):
        """Set the search tool for the factory.
        
        Args:
            search_tool: The search tool instance to use
        """
        self.search_tool = search_tool

    def create_agent(
        self, role: str, goal: str, backstory: str, allow_delegation: bool, tools: List
    ) -> Agent:
        """Creates a specialized agent with defined characteristics.

        Args:
            role (str): Agent's specialized role
            goal (str): Agent's primary objective
            backstory (str): Agent's background and expertise
            allow_delegation (bool): Whether agent can delegate tasks
            tools (List): List of tools available to agent

        Returns:
            Agent: Configured agent instance
        """
        # Wrap tools with callback functionality if callback exists
        if self.tool_callback:
            wrapped_tools = []
            for current_tool in tools:
                original_run = current_tool._run

                def wrapped_run(*args, **kwargs):
                    result = original_run(*args, **kwargs)
                    self.tool_callback(current_tool.__class__.__name__, result)
                    return result

                current_tool._run = wrapped_run
                wrapped_tools.append(current_tool)
        else:
            wrapped_tools = tools

        # Create and return the agent
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            tools=wrapped_tools,
            llm=self.llm,
            verbose=True,
        )

    def create_researcher_agent(self) -> Agent:
        """Creates a surveillance and digital rights research specialist agent.

        This agent focuses on gathering and analyzing current information about
        surveillance systems, privacy violations, and social control mechanisms.

        Returns:
            Agent: Configured researcher agent
        """
        if not self.search_tool:
            raise ValueError("Search tool not initialized. Call set_search_tool first.")

        return self.create_agent(
            role="Digital Surveillance Intelligence Analyst",
            goal="""Uncover and analyze recent (2024) recent cases of technological surveillance systems, privacy 
            violations, and social control mechanisms that mirror themes from '1984'. 
            Focus on government surveillance, corporate data collection, disinformation campaigns, and social media monitoring.""",
            backstory="""Expert analyst with deep expertise in digital privacy, mass surveillance 
            technologies, and civil liberties. Former cybersecurity consultant who has worked with 
            privacy advocacy groups and investigated major data collection scandals. Known for 
            connecting complex technological systems to their societal implications. A huge fan of '1984'""",
            allow_delegation=False,
            tools=[self.search_tool],
        )

    def create_writer_agent(self) -> Agent:
        """Creates a specialized political analysis journalist agent.

        This agent analyzes research findings and creates compelling narratives
        comparing modern surveillance with Orwell's predictions.

        Returns:
            Agent: Configured writer agent
        """
        return self.create_agent(
            role="Dystopian Literature and Political Analysis Expert",
            goal="""Craft compelling, evidence-based narratives that illuminate parallels 
            between modern surveillance practices and Orwell's predictions. Analyze how 
            current events reflect concepts like doublethink, thoughtcrime, and the 
            surveillance state.""",
            backstory="""Distinguished political journalist with expertise in dystopian 
            literature and surveillance politics. Has published acclaimed analyses on digital 
            authoritarianism and modern privacy rights. Skilled at making complex political 
            concepts accessible to general audiences while maintaining analytical depth.""",
            allow_delegation=True,
            tools=[],
        )

    def create_illustrator_agent(self) -> Agent:
        """Creates a conceptual artist specializing in surveillance themes.

        This agent creates visual concepts that represent the parallels between
        modern surveillance society and '1984'.

        Returns:
            Agent: Configured illustrator agent
        """
        return self.create_agent(
            role="Surveillance Culture Visual Analyst",
            goal="""Create powerful visual narratives that capture the parallels between 
            '1984' and modern surveillance society. Focus on symbolic representation of 
            digital monitoring, data collection, and social control mechanisms.""",
            backstory="""Award-winning conceptual artist known for work exploring themes 
            of surveillance capitalism and digital privacy. Has created influential 
            exhibitions on the intersection of technology and personal freedom. Expert 
            in translating complex surveillance concepts into striking visual metaphors.""",
            allow_delegation=False,
            tools=[],
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
                expected_output="Detailed report of the recent cases with source URLs and key parallels to '1984' themes",
            ),
            Task(
                description="""Write a compelling 700-1000 word analysis that:
                1. Introduces the concept of modern surveillance and control
                2. Presents the researched examples and their implications
                3. Draws specific parallels to Orwell's '1984' predictions
                4. Discusses implications for future privacy and freedom
                5. Concludes with recommendations for protecting individual privacy""",
                agent=self.agents["writer"],
                expected_output="Well-structured article with clear sections, supporting evidence, and thought-provoking analysis, in markdown format",
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
            n_results=config.search_results, country=config.country, api_key=SERPER_API_KEY
        )
        agent_factory = AgentFactory(llm)
        agent_factory.set_search_tool(search_tool)

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
#  Disabled for quick launch  while testing
            lanning=True,
            planning_llm=LLM(model="github/gpt-4o")
        )

        # Execute crew and save results
        result = crew.kickoff()
        print(f"""Analysis completed successfully using {config.llm_model}

        ***************************************************************************

        {result}

        ***************************************************************************
        """)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
