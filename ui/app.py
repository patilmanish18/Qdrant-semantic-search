
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Load .env from the project root, not the ui directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "semantic_demo")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

st.set_page_config(
    page_title="Semantic Search",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.5rem 0 1rem 0;
    }
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 0.4rem;
    }
    .hero p {
        color: #64748b;
        font-size: 1.05rem;
    }
    .result-card {
        padding: 1.2rem;
        border: 1px solid rgba(128, 128, 128, 0.28);
        border-radius: 14px;
        margin-bottom: 0.9rem;
    }
    .result-category {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .result-title {
        font-size: 1.15rem;
        font-weight: 650;
        margin: 0.4rem 0;
    }
    .result-description {
        color: #64748b;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading embedding model...")
def load_model():
    return SentenceTransformer(MODEL_NAME)


@st.cache_resource
def load_client():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise ValueError(
            "QDRANT_URL and QDRANT_API_KEY must be configured in .env."
        )

    return QdrantClient(
        url=url,
        api_key=api_key,
        timeout=20,
    )


def search_products(query, limit):
    model = load_model()
    client = load_client()

    if not client.collection_exists(COLLECTION_NAME):
        raise ValueError(
            f"Collection '{COLLECTION_NAME}' was not found in Qdrant."
        )

    vector = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    return response.points


# Sidebar
with st.sidebar:
    st.markdown("## 🔎 Search settings")
    result_limit = st.slider(
        "Number of results",
        min_value=3,
        max_value=10,
        value=5,
    )

    st.divider()
    st.markdown("### About this project")
    st.caption("Semantic search powered by Qdrant and Sentence Transformers.")
    st.caption(f"Collection: `{COLLECTION_NAME}`")
    st.caption("Embedding model: `all-MiniLM-L6-v2`")
    st.caption("Vector size: 384 dimensions")

    st.divider()
    st.caption("Search results are ranked by vector similarity.")


# Main page
st.markdown(
    """
    <div class="hero">
        <h1>Semantic Search Engine</h1>
        <p>Find products by meaning, intent, and context—not just keywords.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("semantic_search_form"):
    query = st.text_input(
        "What are you looking for?",
        placeholder="e.g. A comfortable chair for long hours at a desk",
    )

    submitted = st.form_submit_button(
        "🔎 Search products",
        type="primary",
        use_container_width=True,
    )

st.caption(
    "Try: a laptop for programming · headphones for noisy environments "
    "· a desk for a small home office"
)

if submitted:
    if not query.strip():
        st.warning("Enter a search query to get started.")
    else:
        try:
            with st.spinner("Finding semantically relevant products..."):
                results = search_products(query.strip(), result_limit)

            st.session_state["last_query"] = query.strip()
            st.session_state["last_results"] = [
                {
                    "name": (r.payload or {}).get("name", "Unnamed product"),
                    "category": (r.payload or {}).get("category", "Uncategorized"),
                    "description": (r.payload or {}).get("description", ""),
                    "score": float(r.score),
                }
                for r in results
            ]

        except Exception as exc:
            st.error(
                "Search failed. Check your Qdrant connection, collection "
                "configuration, and embedding model."
            )
            with st.expander("Technical details"):
                st.code(str(exc))

if "last_results" in st.session_state:
    results = st.session_state["last_results"]
    previous_query = st.session_state["last_query"]

    st.divider()
    st.subheader("Search results")
    st.caption(f'Results for: "{previous_query}" · {len(results)} matches')

    if not results:
        st.info("No matching products were returned. Try another query.")
    else:
        for index, product in enumerate(results, start=1):
            with st.container(border=True):
                left, right = st.columns([5, 1])

                with left:
                    st.caption(
                        f"#{index} · {product['category'].upper()}"
                    )
                    st.markdown(f"### {product['name']}")
                    st.write(product["description"])

                with right:
                    st.metric(
                        "Similarity",
                        f"{product['score']:.3f}",
                    )

    st.caption(
        "Similarity scores indicate vector similarity, not a probability "
        "of relevance."
    )
else:
    st.info(
        "Enter a natural-language query above to discover relevant products."
    )
