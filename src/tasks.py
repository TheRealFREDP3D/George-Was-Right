from typing import List, Dict
from crewai import Agent, Task


class TaskManager:
    """
    Manages the creation and organization of tasks for the multi-agent system.

    This class provides a flexible and configurable approach to defining
    tasks for agents analyzing surveillance and privacy issues.
    """

    def __init__(self, agents: Dict[str, Agent]):
        """
        Initialize TaskManager with a dictionary of agents.

        Args:
            agents (Dict[str, Agent]): Dictionary of agents keyed by their role
        """
        self.agents = agents

    def create_tasks(self) -> List[Task]:
        """
        Create a comprehensive set of tasks for the crew.

        Returns:
            List of Task objects to be executed by the crew
        """
        return [
            self._create_research_task(),
            self._create_writing_task(),
            self._create_illustration_task(),
        ]

    def _create_research_task(self) -> Task:
        """
        Create a detailed research task for gathering surveillance information.

        Returns:
            Task focused on researching modern surveillance practices
        """
        return Task(
            description="""Conduct an in-depth investigation of contemporary surveillance practices:
            1. Analyze global government surveillance programs
            2. Explore digital privacy breaches and corporate data collection
            3. Investigate social media monitoring and censorship techniques
            4. Document state-sponsored misinformation campaigns
            
            Requirements:
            - Provide verifiable sources and direct URLs
            - Highlight specific parallels to Orwell's '1984'
            - Focus on events and developments from 2024
            - Maintain a critical and analytical approach""",
            agent=self.agents["researcher"],
            expected_output="""Comprehensive research report including:
            - Detailed analysis of surveillance mechanisms
            - At least 5 concrete examples with source citations
            - Clear connections to themes from '1984'
            - Summary of implications for individual privacy and freedom""",
        )

    def _create_writing_task(self) -> Task:
        """
        Create a writing task to analyze and contextualize research findings.

        Returns:
            Task focused on creating an analytical article
        """
        return Task(
            description="""Develop a compelling 700-1000 word analytical piece that:
            1. Synthesize research findings on modern surveillance
            2. Draw explicit parallels to Orwell's '1984'
            3. Provide critical analysis of current privacy challenges
            4. Explore potential future implications
            5. Offer constructive recommendations for protecting individual privacy
            
            Writing Guidelines:
            - Use clear, accessible language
            - Incorporate specific research examples
            - Maintain an objective yet engaging tone
            - Format document in markdown
            - Include appropriate citations""",
            agent=self.agents["writer"],
            expected_output="""Markdown-formatted article with:
            - Engaging introduction
            - Comprehensive analysis section
            - Specific examples and evidence
            - Thoughtful conclusions and recommendations
            - Proper formatting and readability""",
        )

    def _create_illustration_task(self) -> Task:
        """
        Create a task for generating illustrative concepts.

        Returns:
            Task focused on creating visual representations of surveillance themes
        """
        return Task(
            description="""Generate two sets of detailed illustration prompts:
            
            Modern Surveillance Scenario Prompts:
            - Visualize pervasive digital monitoring
            - Represent data collection and privacy invasion
            - Highlight the omnipresence of technological surveillance
            
            '1984' Parallel Prompts:
            - Recreate iconic scenes from Orwell's novel
            - Draw symbolic connections between historical and modern surveillance
            - Emphasize the psychological impact of constant monitoring
            
            Illustration Requirements:
            - Create two distinct yet thematically linked sets of prompts
            - Focus on symbolic and metaphorical representations
            - Capture the emotional and psychological essence of surveillance""",
            agent=self.agents["illustrator"],
            expected_output="""Comprehensive illustration prompt set:
            - 3-5 detailed prompts for modern surveillance scenario
            - 3-5 detailed prompts referencing '1984'
            - Clear descriptions of visual metaphors
            - Potential artistic approaches and symbolic elements""",
        )
