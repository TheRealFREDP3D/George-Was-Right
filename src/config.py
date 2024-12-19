from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class Settings:
    """
    Configuration settings for the application.
    """

    @staticmethod
    def get_llm():
        """
        Get the language model.
        """
        # Placeholder for actual implementation
        return LLM(
            model="hf:uihui-ai/Llama-3.3-70B-Instruct-abliterated",
            base_url="https://glhf.chat/api/openai/v1",
        )  # Assuming LLM requires a 'model' parameter

    @staticmethod
    def validate():
        """
        Validate the configuration settings.
        """
        required_env_vars = ["LLM_MODEL", "LLM_BASE_URL"]
        for var in required_env_vars:
            if not os.getenv(var):
                raise ValueError(f"Missing environment variable: {var}")

    # SerperSearchTool settings
    @staticmethod
    def get_serper_search_tool_settings():
        """
        Get the SerperSearchTool settings.
        """
        n_results = int(os.getenv("SERPER_SEARCH_N_RESULTS", 10))
        country = os.getenv("SERPER_SEARCH_COUNTRY", "us")
        api_key = os.getenv("SERPER_API_KEY")
        return {
            "n_results": n_results,
            "country": country,
            "api_key": api_key,
        }

    # Agent Settings
    MAX_RPM = int(os.getenv("MAX_RPM", 10))  # Maximum requests per minute

    # Planning Settings
    PLANNING = (
        os.getenv("PLANNING", "True").lower() == "true"
    )  # Enable or disable planning

    # Validate the configuration settings
    validate()

    # Get the language model
    LLM = get_llm()

    # Get the SerperSearchTool settings
    SERPER_SEARCH_TOOL_SETTINGS = get_serper_search_tool_settings()
    # Search Results to Return
    SEARCH_RESULTS = 10

    # Country
    COUNTRY = "US"

    # Agent Settings
    MAX_RPM = 10

    # Planning Settings
    PLANNING = True
