# Qdrant Semantic Search Engine

A semantic product search application built with **Python, Qdrant Cloud, Sentence Transformers, and Streamlit**. Search a product catalog using natural language and retrieve relevant results based on vector similarity rather than relying solely on exact keyword matches.

## Overview

Traditional keyword search often struggles when users describe what they need differently from how a product is named. This project uses text embeddings and vector similarity search to retrieve products based on the meaning of a query.

For example, searching for *"a comfortable chair for long hours at a desk"* can retrieve ergonomic office chairs even when the query doesn't contain the exact product name.

## Key Features

- **Semantic retrieval:** Search products using natural-language queries.
- **Vector database:** Store embeddings and product metadata in Qdrant Cloud.
- **Text embeddings:** Use the pretrained `all-MiniLM-L6-v2` model to generate 384-dimensional vectors.
- **Batch ingestion:** Load product records from CSV and upsert them into Qdrant in batches.
- **Interactive web interface:** Explore ranked results using Streamlit.
- **Command-line search:** Test semantic retrieval directly from the terminal.
- **Reproducible ingestion:** Use stable product IDs to update existing points on repeated runs.
- **Configurable result count:** Choose how many results to retrieve.
- **Secure configuration:** Load credentials from environment variables rather than hardcoding secrets.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data ingestion |
| Qdrant Cloud | Vector storage and similarity search |
| Sentence Transformers | Text embedding generation |
| `all-MiniLM-L6-v2` | Sentence embedding model |
| Streamlit | Web user interface |
| CSV | Product catalog storage |
| `python-dotenv` | Environment configuration |

## Architecture

```text
Product Catalog (CSV)
        |
        v
generate_data.py
        |
        v
populate.py
        |
        v
Sentence Transformer
384-dimensional embeddings
        |
        v
Qdrant Cloud
Collection: semantic_demo
        ^
        |
Vector similarity search
        ^
        |
User's natural-language query
        |
        +----------------------+
        |                      |
        v                      v
    search.py              ui/app.py
    CLI Search           Streamlit UI
```

## Project Structure

```text
Qdrant_project/
├── data/
│   └── products.csv
├── ui/
│   └── app.py
├── .env.example
├── .gitignore
├── check_vectors.py
├── generate_data.py
├── populate.py
├── requirements.txt
├── search.py
├── setup_semantic_search.py
└── README.md
```

The `.env` file and `.venv/` directory are intentionally excluded from version control.

## Getting Started

### Prerequisites

- Python 3.10 or a version compatible with the installed dependencies
- A Qdrant Cloud account and configured cluster
- Git
- Internet access for Qdrant Cloud and model downloads

### 1. Clone the repository

After publishing the project, replace the placeholders with your GitHub username and repository name.

```bash
git clone https://github.com/YOUR_USERNAME/qdrant-semantic-search.git
cd qdrant-semantic-search
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Qdrant Cloud

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your own Qdrant Cloud credentials:

```dotenv
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=semantic_demo
```

Never commit `.env` or expose your API key publicly.

### 5. Generate the dataset

```powershell
python generate_data.py
```

This creates `data/products.csv` for development and experimentation.

### 6. Create the collection

```powershell
python setup_semantic_search.py
```

The semantic search collection uses 384-dimensional vectors and cosine distance.

### 7. Ingest products

```powershell
python populate.py
```

The ingestion script reads the CSV, generates embeddings, and upserts products into Qdrant in batches.

### 8. Run command-line search

```powershell
python search.py
```

Enter a natural-language query. Type `exit` to end the session.

### 9. Launch the Streamlit interface

```powershell
python -m streamlit run ui/app.py
```

Open the local URL displayed in the terminal, typically:

`http://localhost:8501`

## Example Search Queries

Try queries such as:

- A supportive chair for working at a computer all day
- A portable computer for software development
- Wireless headphones for online meetings in noisy environments
- A portable drive for backing up programming projects
- A compact desk for a small home office

The application returns the closest matches according to vector similarity.

## How It Works

1. **Data preparation:** Product records are stored in a structured CSV file.
2. **Embedding generation:** The Sentence Transformers model converts product text into dense vectors.
3. **Vector storage:** Qdrant stores the vectors and associated product metadata.
4. **Query embedding:** The same embedding model converts the user's search query into a vector.
5. **Similarity retrieval:** Qdrant ranks products by cosine similarity.
6. **Result presentation:** The CLI or Streamlit UI displays product information and similarity scores.

The ingestion and search workflows must use a consistent embedding model, vector dimension, and compatible text preprocessing.

## Dataset and Limitations

The project uses a **synthetic product catalog** generated for development and demonstration. Product listings are not a verified commercial inventory.

The quality of semantic retrieval depends on the diversity and accuracy of the product descriptions. Similar descriptions may produce similar scores, and a high similarity score does not guarantee that a result is relevant.

The current project is a focused semantic search implementation, not a complete e-commerce platform. It does not provide product purchasing, inventory management, user authentication, or a calibrated relevance probability.

## Security

- Keep credentials in `.env`.
- Exclude `.env` and `.venv/` from Git.
- Never commit API keys or secrets.
- Rotate credentials if they are exposed.
- Review staged files before committing.

## Future Improvements

- Evaluate retrieval quality against a curated set of test queries.
- Improve dataset diversity using a properly licensed dataset.
- Add category filtering to the search interface.
- Add automated tests for ingestion and retrieval.
- Improve logging and error handling.
- Deploy the Streamlit application for public demonstration.

## License

A license has not yet been specified. Add an appropriate license before permitting reuse or redistribution of the project.
