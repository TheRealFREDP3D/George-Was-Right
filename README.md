# **George-Was-Right | v1.5 | README.md**

## **Overview**

This project uses CrewAI to analyze current events in relation to themes from George Orwell's "1984". It orchestrate three agents (Researcher, Writer, Illustrator) to perform tasks such as searching for relevant news, comparing news with "1984" themes, writing articles, and generating illustration prompts.

---

## **Prerequisites**

- Python 3.8 or later
- crewai and crewai-tools libraries
- SerperDevTool API key (add to .env file)
- LLM providerAPI key (add to .env file or set as environment variable)

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

## **Output**

The file name will be the name of the LLM model used, and the file extension will be `.md`. The file will contain the results of the analysis.

## **Configuration**

You can configure the script by modifying the following environment variables in your `.env` file:

- `HOW_MANY_RESULTS`: The number of search results to retrieve.
- `COUNTRY`: The country to focus on for the search.
- `LLM_MODEL`: The large language model to use (e.g., `groq/mixtral-8x7b-32768`).

## **Known Issues**

- Error handling could be improved.
- The script relies on a specific LLM model, which may change or become unavailable.
- The output file path is hardcoded; consider making it more flexible.
- Merge conflicts should be resolved before committing changes.

## **Future Development**

- Implement enhanced error handling and logging.
- Add flexibility to output file path configuration.
- Explore additional LLM models for broader analysis capabilities.
- Improve prompt engineering for better results.
- Allow for more flexible LLM model selection.
- Enhance output formatting and visualization.

---

[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)
