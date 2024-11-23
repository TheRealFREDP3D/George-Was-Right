<<<<<<< HEAD
<<<<<<< HEAD
=======
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
    LLM_MODEL = "groq/mixtral-8x7b-32768"


# Load environment variables
dotenv.load_dotenv()

# Initialize agentops
agentops.init()

# Initialize the search tool
search_tool = SerperDevTool(n_results=Config.SEARCH_RESULTS, country=Config.COUNTRY)


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
            tools=[search_tool],
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
            tools=[search_tool],
            cache=True,
            llm=self.llm,
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
            llm=self.llm,
        )


class TaskManager:
    """Manages the creation and organization of tasks."""

    @staticmethod
    def create_tasks(agents: dict) -> List[Task]:
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
                agent=agents["researcher"],
                expected_output="Detailed report of 3-5 recent cases with source URLs and key parallels to '1984' themes",
            ),
            Task(
                description="""Write a compelling 700-1000 word analysis that:
                1. Introduces the concept of modern surveillance and control
                2. Presents the researched examples and their implications
                3. Draws specific parallels to Orwell's '1984' predictions
                4. Discusses the societal impact and potential future implications
                5. Concludes with recommendations for maintaining individual privacy and freedom""",
                agent=agents["writer"],
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
                agent=agents["illustrator"],
                expected_output="Two detailed, contrasting illustration prompts that effectively visualize the comparison",
            ),
        ]


def main():
    """Main execution flow."""
    # Initialize core components
    llm = LLM(model=Config.LLM_MODEL)
    agent_factory = AgentFactory(llm)

    # Create agents
    agents = {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }

    # Create and execute crew
    tasks = TaskManager.create_tasks(agents)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True,
        llm=Config.LLM_MODEL,
        planning=True,
        planning_llm=Config.LLM_MODEL,
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
        print(f"An error occurred while executing the crew: {str(e)}")


if __name__ == "__main__":
    main()
=======
<<<<<<< HEAD
>>>>>>> be06bdd (modified:   main.py)
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
    LLM_MODEL = "groq/llama3-70b-8192"


# Load environment variables
dotenv.load_dotenv()

# Initialize agentops
agentops.init()

# Initialize the search tool
search_tool = SerperDevTool(n_results=Config.SEARCH_RESULTS, country=Config.COUNTRY)


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
            tools=[search_tool],
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
            tools=[search_tool],
            cache=True,
            llm=self.llm,
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
            llm=self.llm,
        )


class TaskManager:
    """Manages the creation and organization of tasks."""

    @staticmethod
    def create_tasks(agents: dict) -> List[Task]:
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
                agent=agents["researcher"],
                expected_output="Detailed report of 3-5 recent cases with source URLs and key parallels to '1984' themes",
            ),
            Task(
                description="""Write a compelling 700-1000 word analysis that:
                1. Introduces the concept of modern surveillance and control
                2. Presents the researched examples and their implications
                3. Draws specific parallels to Orwell's '1984' predictions
                4. Discusses the societal impact and potential future implications
                5. Concludes with recommendations for maintaining individual privacy and freedom""",
                agent=agents["writer"],
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
                agent=agents["illustrator"],
                expected_output="Two detailed, contrasting illustration prompts that effectively visualize the comparison",
            ),
        ]


def main():
    """Main execution flow."""
    # Initialize core components
    llm = LLM(model=Config.LLM_MODEL)
    agent_factory = AgentFactory(llm)

    # Create agents
    agents = {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }

    # Create and execute crew
    tasks = TaskManager.create_tasks(agents)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True,
        llm=Config.LLM_MODEL,
        planning=True,
        planning_llm=Config.LLM_MODEL,
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
        print(f"An error occurred while executing the crew: {str(e)}")


if __name__ == "__main__":
    main()
=======
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
    LLM_MODEL = "github/gpt-4o"


# Load environment variables
dotenv.load_dotenv()

# Initialize agentops
agentops.init()

# Initialize the search tool
search_tool = SerperDevTool(n_results=Config.SEARCH_RESULTS, country=Config.COUNTRY)


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
            tools=[search_tool],
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
            tools=[search_tool],
            cache=True,
            llm=self.llm,
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
            llm=self.llm,
        )


class TaskManager:
    """Manages the creation and organization of tasks."""

    @staticmethod
    def create_tasks(agents: dict) -> List[Task]:
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
                agent=agents["researcher"],
                expected_output="Detailed report of 3-5 recent cases with source URLs and key parallels to '1984' themes",
            ),
            Task(
                description="""Write a compelling 700-1000 word analysis that:
                1. Introduces the concept of modern surveillance and control
                2. Presents the researched examples and their implications
                3. Draws specific parallels to Orwell's '1984' predictions
                4. Discusses the societal impact and potential future implications
                5. Concludes with recommendations for maintaining individual privacy and freedom""",
                agent=agents["writer"],
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
                agent=agents["illustrator"],
                expected_output="Two detailed, contrasting illustration prompts that effectively visualize the comparison",
            ),
        ]


def main():
    """Main execution flow."""
    # Initialize core components
    llm = LLM(model=Config.LLM_MODEL)
    agent_factory = AgentFactory(llm)

    # Create agents
    agents = {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }

    # Create and execute crew
    tasks = TaskManager.create_tasks(agents)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True,
        llm=Config.LLM_MODEL,
        planning=True,
        planning_llm=Config.LLM_MODEL,
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
        print(f"An error occurred while executing the crew: {str(e)}")


if __name__ == "__main__":
    main()
>>>>>>> d86e314 (deleted:    agentops.log (#22))
