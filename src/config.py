import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()


class Settings:
    """Centralized configuration management."""

    # Core Application Settings
    APP_NAME: str = "George Was Right"
    VERSION: str = "0.1.0"

    # Timestamp for unique file naming and logging
    TIMESTAMP: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Search Configuration
    COUNTRY: str = os.getenv("SEARCH_COUNTRY", "us")
    SEARCH_RESULTS: int = int(os.getenv("SEARCH_RESULTS", 3))

    # API Keys (with error handling)
    SERPER_API_KEY: Optional[str] = os.getenv("SERPER_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # LLM Configuration
    @classmethod
    def get_llm(cls) -> LLM:
        """
        Dynamic LLM configuration with fallback mechanisms.

        Returns:
            Configured LLM instance

        Raises:
            ValueError: If no valid LLM configuration is found
        """
        model_name = os.getenv("LLM_MODEL", "hf:Qwen/QwQ-32B-Preview")
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL", "https://glhf.chat/api/openai/v1")

        if not api_key:
            raise ValueError("No API key configured for the language model")

        return LLM(model=model_name, api_key=api_key, base_url=base_url)

    @classmethod
    def validate(cls):
        """
        Validate critical configuration parameters.

        Raises:
            ValueError: If any critical configuration is missing
        """
        if not cls.SERPER_API_KEY:
            raise ValueError("Serper API key is required")

        if not cls.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required")


# Optional logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=f"logs/{Settings.TIMESTAMP}_app.log",
)
logger = logging.getLogger(__name__)
