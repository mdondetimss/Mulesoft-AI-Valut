## Running the Jira AI Bug Agent

Follow the steps below to run the project locally using **Anypoint Code Builder** and Streamlit.



## 1. Clone the Repository

```bash
git clone <repository_url>
cd <repo-name>
```



## 2. Configure Mule Credentials

Place the following files inside:

```
src/main/resources
```

### 2.1 connections.yaml

```yaml
jira:
  user: your-email@example.com
  api-token: YOUR_JIRA_API_TOKEN
  url: https://your-domain.atlassian.net
```



### 2.2 envVars.json

Provide the credentials for the AI provider(s) you plan to use.

```json
{
  "OPENAI": {
    "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"
  },
  "MISTRAL_AI": {
    "MISTRAL_AI_API_KEY": "YOUR_MISTRAL_AI_API_KEY"
  },
  "OLLAMA": {
    "OLLAMA_BASE_URL": "http://baseurl.ollama.com"
  },
  "GROQAI_OPENAI": {
    "GROQ_API_KEY": "YOUR_GROQAI_API_KEY"
  },
  "ANTHROPIC": {
    "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY"
  },
  "AZURE_OPENAI": {
    "AZURE_OPENAI_KEY": "YOUR_AZURE_OPENAI_KEY",
    "AZURE_OPENAI_ENDPOINT": "https://endpoint.azure.com",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "YOUR_DEPLOYMENT_NAME"
  },
  "HUGGING_FACE": {
    "HUGGING_FACE_API_KEY": "YOUR_HUGGING_FACE_API_KEY"
  },
  "GEMINI_AI": {
    "GEMINI_AI_KEY": "YOUR_GEMINI_AI_KEY"
  }
}
```



## 3. Open in Anypoint Code Builder

Open the project folder in **Anypoint Code Builder**.

Ensure the root folder contains:

* `pom.xml`
* `src/main/mule`
* `src/main/resources`



## 4. Build and Run the Mule Application

Open the integrated terminal and run:

```bash
mvn clean package
mvn mule:run
```

Wait until the logs show the application has started and the HTTP listener is running.

Leave this process running.



## 5. Set Up the Python Environment

Open a new terminal and navigate to the Python folder (where `frontend.py` exists):

```bash
cd python
```

### 5.1 Install Dependencies

Sync project dependencies and create the virtual environment:

```bash
uv sync
```

This will install all required packages into the `.venv` directory.



### 5.2 Configure Frontend Environment

Inside the same Python folder, create a file named:

```
.env
```

Add:

```
MULE_API_URL=<URL>
```




## 6. Run the Frontend

From inside the Python folder:

```bash
uv run streamlit run frontend.py
```

Open the local URL displayed in the terminal.


## 7. Test the Application

1. Enter a Jira Issue ID, Summary, and Description in the Streamlit UI.
2. Submit.
3. The application will:

   * Generate AI summary
   * Perform sentiment analysis
   * Update the Jira issue
   * Display the results in the UI



## 8. Stop the Application

To stop:

* Press `Ctrl + C` in both terminals.



## 9. Known Issues & Workarounds

* If the following commands fail:

  ```bash
  mvn clean package
  mvn mule:run
  ```

  Run the Mule application directly from **VS Code / Anypoint Code Builder**:

  * Open the **Run** tab.
  * Click **Run Without Debugging**.



* If Streamlit does not start using:

  ```bash
  uv run streamlit run frontend.py
  ```

  Try one of the following alternatives:

  ```bash
  uv run python -m streamlit run frontend.py
  ```

  or

  ```bash
  uv run py -m streamlit run frontend.py
  ```
