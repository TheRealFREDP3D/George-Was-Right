import logging
from typing import Any, Callable, Optional

from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from rich.console import Console
from rich.logging import RichHandler


class ToolManager:
    """
    Centralized management of tools for AI agents with enhanced logging and configuration.
    """

    def __init__(
        self,
        serper_api_key: Optional[str] = None,
        max_search_results: int = 3,
        country: str = "us",
    ):
        """
        Initialize tool manager with configurable search parameters.

        Args:
            serper_api_key (Optional[str]): API key for Serper search service
            max_search_results (int): Maximum number of search results to retrieve
            country (str): Country code for search localization
        """
        self._serper_api_key = serper_api_key
        self._max_search_results = max_search_results
        self._country = country

        # Rich console for enhanced terminal output
        self._console = Console()

        # Configure logging with Rich handler
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(console=self._console, rich_tracebacks=True)],
        )
        self._logger = logging.getLogger("ToolManager")

    def create_search_tool(self) -> SerperDevTool:
        """
        Create a configured Serper search tool.

        Returns:
            Configured SerperDevTool instance

        Raises:
            ValueError: If Serper API key is not provided
        """
        if not self._serper_api_key:
            raise ValueError("Serper API key is required to create search tool")

        try:
            return SerperDevTool(
                n_results=self._max_search_results,
                country=self._country,
                api_key=self._serper_api_key,
            )
        except Exception as e:
            self._logger.error(f"Failed to create search tool: {e}")
            raise

    def create_website_search_tool(self) -> WebsiteSearchTool:
        """
        Create a website search tool for deep web searches.

        Returns:
            Configured WebsiteSearchTool instance
        """
        return WebsiteSearchTool()

    def create_website_scraper(self, url: str) -> ScrapeWebsiteTool:
        """
        Create a website scraping tool for specific URL.

        Args:
            url (str): URL to be scraped

        Returns:
            Configured ScrapeWebsiteTool instance
        """
        return ScrapeWebsiteTool(url=url)

    def wrap_tool_with_logging(self, tool: Any, name: Optional[str] = None) -> Any:
        """
        Wrap a tool with logging functionality to track its usage and outputs.

        Args:
            tool (Any): Tool to be wrapped
            name (Optional[str]): Custom name for the tool, defaults to tool's class name

        Returns:
            Tool with additional logging capabilities
        """
        tool_name = name or tool.__class__.__name__

        def log_tool_usage(method):
            def wrapper(*args, **kwargs):
                try:
                    self._logger.info(f"Using tool: {tool_name}")
                    result = method(*args, **kwargs)
                    self._logger.info(f"Tool {tool_name} completed successfully")
                    return result
                except Exception as e:
                    self._logger.error(f"Error in tool {tool_name}: {e}")
                    raise

            return wrapper

        # Dynamically wrap the tool's run method with logging
        tool._run = log_tool_usage(tool._run)
        return tool

    def create_custom_tool(self, name: str, description: str, function: Callable):
        """
        Create a custom tool with a specific function and description.

        Args:
            name (str): Name of the tool
            description (str): Description of the tool's purpose
            function (Callable): Function to be executed by the tool

        Returns:
            A custom tool object with logging capabilities
        """

        class CustomTool:
            def __init__(self, func, desc):
                self._run = func
                description = desc

        custom_tool = CustomTool(function, description)
        return self.wrap_tool_with_logging(custom_tool, name)


# Utility functions
def validate_url(url: str) -> bool:
    """
    Basic URL validation utility.

    Args:
        url (str): URL to validate

    Returns:
        bool: Whether the URL is valid
    """
    import re

    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return url_pattern.match(url) is not None
