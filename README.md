# **George-Was-Right | v1.5 | README.md**

## **Overview**

This project uses CrewAI to analyze current events in relation to themes from George Orwell's "1984". It orchestrate three agents (Researcher, Writer, Illustrator) to perform tasks such as searching for relevant news, comparing news with "1984" themes, writing articles, and generating illustration prompts.

---

## **Architecture**

The project follows a modular architecture with three main components:

### Core Components

1. **Config**: Central configuration class that manages:
   - Timestamps for output files
   - Search parameters (results count, country)
   - LLM model selection

2. **AgentFactory**: Creates specialized AI agents:
   - Researcher: Surveillance and digital rights specialist
   - Writer: Political analysis journalist
   - Illustrator: Conceptual artist for surveillance themes

3. **TaskManager**: Orchestrates tasks between agents:
   - Creates and assigns tasks to agents
   - Manages task dependencies and workflow

### Workflow

1. System initialization with configuration
2. Agent creation through AgentFactory
3. Task creation and assignment
4. Crew execution of tasks
5. Result analysis and output generation

### Dependencies

- **crewai**: Core framework for agent management
- **crewai_tools**: Additional tools for agent capabilities
- **python-dotenv**: Environment configuration
- **rich**: Enhanced terminal output
- **agentops**: Operations monitoring
- **SerperDev API**: Web search capabilities

---

## **Prerequisites**

- Python 3.8 or later
- crewai and crewai-tools libraries
- SerperDevTool API key (add to .env file)
- LLM providerAPI key (add to .env file or set as environment variable)

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/George-Was-Right.git
   cd George-Was-Right
   ```

2. Install dependencies:
   ```bash
   # Using pip
   pip install -r requirements.txt

   # Or using Pipenv
   pipenv install
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```shell
     SERPER_API_KEY=your_serper_api_key
     LLM_PROVIDER_API_KEY=your_llm_api_key
     ```

---

## **Usage**

- Install required libraries: `pip install dotenv rich crewai crewai-tools`
- Create a `.env` file with the necessary API keys:

```shell
# example: /.env
SERPER_API_KEY=<YOUR_API_KEY>
<LLM_PROVIDER_API_KEY>=<YOUR_API_KEY>
```

- Run the script: `python main.py`

---

## **Configuration Options**

Modify these constants in `main.py` to customize behavior:

| Parameter | Description | Default |
|-----------|-------------|---------|
| COUNTRY | Target country for search | "ca" |
| LLM_MODEL | LLM model to use | "ollama/gemma2:latest" |
| SEARCH_RESULTS | Number of search results | 5 |

---

## **Usage Examples**

1. Basic usage:
   ```bash
   python main.py
   ```

2. View output:
   - Results are saved in markdown format
   - Filename format: `[LLM_MODEL]-[TIMESTAMP].md`
   - Location: `./logs/[LLM_MODEL]/`

---

## **Output**

The file name will be the name of the LLM model used, and the file extension will be `.md`. The file will contain the results of the analysis.

---

## **Configuration**

You can configure the script by modifying the following constants:

- `HOW_MANY_RESULTS`: The number of search results to retrieve.
- `COUNTRY`: The country to focus on for the search.
- `LLM_MODEL`: The large language model to use.

---

## **Known Issues**

- Error handling could be improved.
- The script relies on a specific LLM model, which may change or become unavailable.
- The output file path is hardcoded; consider making it more flexible.

---

## **Future Development**

- Add more robust error handling and logging.
- [x]Improve prompt engineering for better results.
- Allow for more flexible LLM model selection.
- Enhance output formatting and visualization.

---

## **Contributing**

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## **Troubleshooting**

Common issues and solutions:

1. **API Key Issues**:
   - Verify `.env` file exists
   - Check API key format
   - Ensure environment variables are loaded

2. **LLM Model Errors**:
   - Confirm model availability
   - Check model compatibility
   - Verify API credentials

3. **Search Problems**:
   - Validate SerperDev API key
   - Check internet connection
   - Verify search parameters

---

## **License**

This project is licensed under the terms specified in [LICENSE](LICENSE).

---

## **Security**

For security concerns or vulnerability reports, please see [SECURITY.md](SECURITY.md).

---

[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)
