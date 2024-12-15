# **George-Was-Right | v1.5 | README.md**

[![CodeFactor](https://www.codefactor.io/repository/github/therealfredp3d/george-was-right/badge)](https://www.codefactor.io/repository/github/therealfredp3d/george-was-right)

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
