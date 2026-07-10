# LangChain First Project

Study project for building AI agents with LangChain and LangGraph. The main application is a Retrieval-Augmented Generation (RAG) agent that answers questions using local PDF documents.

The project also includes older examples for custom tools, CEP lookup, and SQL database agents.

## Main Features

- RAG agent over local PDF files
- PDF loading with `PyPDFLoader`
- Text chunking with `RecursiveCharacterTextSplitter`
- OpenAI embeddings stored in Chroma
- LangChain agent with a document-search tool
- LangGraph configuration for local development
- Example SQLite database and SQL agent experiments
- Jupyter notebooks for learning and experimentation

## Project Structure

```text
.
├── agent_rag.py              # Main RAG agent
├── langgraph.json            # LangGraph local dev configuration
├── pyproject.toml            # Project dependencies
├── files/                    # Source PDF documents
├── notebooks/                # Learning notebooks
├── db/                       # SQLite database example
└── old/                      # Earlier agent/tool experiments
```

## Requirements

- Python 3.12+
- `uv`
- OpenAI API key

## Setup

Install dependencies:

```bash
uv sync
```

Create a local environment file:

```bash
cp .env-example .env
```

Then edit `.env` and set your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`OPENAI_API_KEY` is required for the main RAG agent. `TAVILY_API_KEY` is included for tool/search experiments.

## Running the RAG Agent

Start LangGraph locally:

```bash
uv run langgraph dev
```

The configured graph is:

```json
{
  "agent": "./agent_rag.py:agent"
}
```

On startup, `agent_rag.py`:

1. Loads PDFs from `files/`
2. Splits the content into chunks
3. Creates or reuses a local Chroma vector store in `chroma_db/`
4. Exposes `search_on_doc` as a tool for the agent
5. Creates an HR assistant agent for Nexus Corp documents

Example questions:

```text
What does the employee handbook say about vacation policy?
```

```text
What information is available about Project Lunar Base Omega?
```

## Source Documents

The RAG agent currently loads:

- `files/employee_handbook_v2.pdf`
- `files/project_lunar_base_omega.pdf`

To use different documents, update the `file_paths` list in `agent_rag.py`.

## Database Example

The `db/` directory contains a sample SQLite store database:

- `db/script.sql` defines the schema
- `db/populate_db.py` inserts sample data
- `db/store.sqlite` is the local database file

Older SQL agent code is available in `old/db_agent.py`.

## Notebooks

The `notebooks/` directory contains exploratory examples:

- `main.ipynb`
- `rag_example.ipynb`
- `rag_pdf.ipynb`

## Notes

- The first RAG run may take longer because embeddings need to be generated.
- The generated Chroma database is stored locally in `chroma_db/`.
- Files in `old/` are learning examples and are not the primary application entry point.
