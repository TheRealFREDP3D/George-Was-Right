from crewai import LLM  # Assuming LLM is part of the crewai module


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
        # Placeholder for actual validation logic
        pass

    # SerperSearchTool settings

    # Search Results to Return
    SEARCH_RESULTS = 10

    # Country
    COUNTRY = "US"

    # Agent Settings
    MAX_RPM = 10

    # Planning Settings
    PLANNING = True
