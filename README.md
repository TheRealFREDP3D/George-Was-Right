```
project: George-Was-Right
file: README.md
author: Frederick Pellerin
email: fredp3d@proton.me
x: https://x.com/TheRealFredP3D
github: https://github.com/TheRealFREDP3D
last_modified: 22-10-2024
```

# George Was Right!

# About the Author



## What is it?

Overall, this script is designed to automate a collaborative task involving researching, writing, and illustrating around contemporary news and their parallels to "1984," while utilizing the capabilities of AI agents configured with specific roles and tools.

---

### Components

#### Imports and Environment Setup

**dotenv**: Used for loading environment variables, which include sensitive data like API keys.
**rich**: Utilized for enhanced console printing.
**CrewAI Framework**: Classes like Agent, Task, Crew, and LLM are part of this framework, providing the functionalities needed for the workflow.
**SerperDevTool**: A custom tool for internet searching within the workflow.

---

#### Configuration Class


A Config dataclass holds configuration settings including the number of search results, country, model used by the LLM, output directory, log file path, and an optional Serper API key.

The llm_model can be configured using environment variables for flexibility.

----

#### Agent Classes

These classes define different roles within the workflow:

**ResearcherAgent**: Tasked with finding news articles that relate to themes of "1984," using internet search tools.
**WriterAgent**: Writes a comparative analysis based on the articles found.
**IllustratorAgent**: Creates illustration prompts based on news events and their thematic links to "1984."

Each agent is initialized with a role, goal, backstory, and optionally tools or LLM configurations.

---

#### Crew Manager

Initializes with the given configuration and manages LLM and search tool setup.
Responsible for creating tasks, setting up the crew with the required agents and tasks, and saving results.

---

#### Main Execution

Retrieves configuration settings, including the API key from an environment variable.

Sets up and starts the workflow.
