from rich import print
import requests
import os

from llm_selector import LLMSelector

# Example 1: Find models with sufficient context window
suitable_models = LLMSelector.find_models_by_context_window(
    min_tokens=10000,
    provider="Groq"  # Optional: filter by provider
)

# Example 2: Get specific model information
model_info = LLMSelector.get_model_info("groq/mixtral-8x7b-32768")

# Example 3: List all available models
all_models = LLMSelector.list_models()

# Get JSON output
json_output = LLMSelector.to_json(suitable_models)

api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print("Raw response:")
print(response.json())

