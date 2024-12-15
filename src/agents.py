from typing import List, Optional, Callable
from crewai import Agent, LLM
from crewai_tools import SerperDevTool


class AgentFactory:
    """
    Advanced agent creation factory with enhanced configurability.

    Provides a centralized mechanism for creating specialized AI agents
    with configurable tools, callbacks, and error handling.
    """

    def __init__(self, llm: LLM, tool_callback: Optional[Callable] = None):
        """
        Initialize AgentFactory with a language model and optional tool callback.

        Args:
            llm (LLM): Language model for agent operations
            tool_callback (Optional[Callable]): Optional callback for tool interactions
        """
        self._llm = llm
        self._tool_callback = tool_callback
        self._search_tool = None

    def set_search_tool(self, search_tool: SerperDevTool):
        """Configure the search tool for agents."""
        self._search_tool = search_tool
        return self

    def _wrap_tools(self, tools: List):
        """
        Wrap tools with optional callback functionality.

        Args:
            tools (List): Original tools to be wrapped

        Returns:
            List of wrapped tools
        """
        if not self._tool_callback:
            return tools

        wrapped_tools = []
        for tool in tools:
            original_run = tool._run

            def wrapped_run(*args, **kwargs):
                result = original_run(*args, **kwargs)
                self._tool_callback(tool.__class__.__name__, result)
                return result

            tool._run = wrapped_run
            wrapped_tools.append(tool)

        return wrapped_tools

    def create_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: List = [],
        allow_delegation: bool = False,
    ) -> Agent:
        """
        Create a versatile agent with comprehensive configuration.

        Args:
            role (str): Agent's professional role
            goal (str): Agent's primary objective
            backstory (str): Agent's background narrative
            tools (List): Available tools for the agent
            allow_delegation (bool): Permission for task delegation

        Returns:
            Configured Agent instance
        """
        wrapped_tools = self._wrap_tools(tools)

        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=wrapped_tools,
            allow_delegation=allow_delegation,
            llm=self._llm,
            verbose=True,
            cache=True,
        )

    def create_researcher_agent(self) -> Agent:
        """Create a specialized digital surveillance research agent."""
        if not self._search_tool:
            raise ValueError(
                "Search tool must be configured before creating researcher agent"
            )

        return self.create_agent(
            role="Digital Surveillance Intelligence Analyst",
            goal="Uncover and analyze modern surveillance systems and privacy violations",
            backstory="Expert privacy and cybersecurity investigator with deep understanding of digital rights",
            tools=[self._search_tool],
            allow_delegation=False,
        )

    def create_writer_agent(self) -> Agent:
        """Create a specialized political analysis journalist agent."""
        return self.create_agent(
            role="Dystopian Literature and Political Analysis Expert",
            goal="Craft compelling narratives about surveillance and privacy",
            backstory="Distinguished political journalist specializing in digital authoritarianism, freedom of speech and government misinformation and propaganda",
            allow_delegation=True,
        )

    def create_illustrator_agent(self) -> Agent:
        """Create a conceptual artist focused on surveillance themes."""
        return self.create_agent(
            role="Surveillance Culture Visual Analyst",
            goal="Create visual narratives exploring surveillance and control",
            backstory="Award-winning conceptual artist examining technology's impact on freedom",
            allow_delegation=False,
        )
