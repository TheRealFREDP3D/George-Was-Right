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

from datetime import datetime
from typing import List, Dict
import dotenv
from rich import print
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# Load environment variables from .env file
dotenv.load_dotenv()

# Global configuration constants
COUNTRY = "ca"  # Target country for search results
LLM_MODEL = "ollama/qwen2.5-coder:latest"  # LLM model identifier
SEARCH_RESULTS = 5  # Number of search results to retrieve


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
search_tool = SerperDevTool(n_results=SEARCH_RESULTS, country=COUNTRY)


class AgentFactory:
    """Factory class for creating specialized AI agents.
    
    This factory creates agents with specific roles, goals, and capabilities
    for analyzing surveillance and privacy issues.
    
    Attributes:
        llm (LLM): Language model instance for agent communication
    """

    def __init__(self, llm: LLM):
        """Initialize the factory with a language model.
        
        Args:
            llm (LLM): Language model instance for agent operations
        """
        self.llm = llm

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
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            verbose=True,
            llm=self.llm,
            cache=True,
            tools=tools,
        )

    def create_researcher_agent(self) -> Agent:
        """Creates a surveillance and digital rights research specialist agent.
        
        This agent focuses on gathering and analyzing current information about
        surveillance systems, privacy violations, and social control mechanisms.
        
        Returns:
            Agent: Configured researcher agent
        """
        return self.create_agent(
            role="Digital Surveillance Intelligence Analyst",
            goal="""Uncover and analyze recent (November 2024) technological surveillance systems, privacy 
            violations, and social control mechanisms that mirror concepts from '1984'. 
            Focus on government surveillance, corporate data collection, and social media monitoring.""",
            backstory="""Expert analyst with deep expertise in digital privacy, mass surveillance 
            technologies, and civil liberties. Former cybersecurity consultant who has worked with 
            privacy advocacy groups and investigated major data collection scandals. Known for 
            connecting complex technological systems to their societal implications.""",
            allow_delegation=False,
            tools=[search_tool],
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
        agent_factory = AgentFactory(llm)

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
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
