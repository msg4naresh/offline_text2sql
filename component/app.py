import os
import streamlit as st
from llama_index.core import Settings, SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sqlalchemy import create_engine
from llama_index.llms.ollama import Ollama


# Function to initialize settings
def initialize_settings():
    Settings.llm = Ollama(model="gemma2:latest", request_timeout=120.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


# Function to get database URI
def get_database_uri():
    host = os.environ.get("PG_HOST", "")
    port = os.environ.get("PG_PORT", "")
    username = os.environ.get("PG_USERNAME", "")
    password = os.environ.get("PG_PASSWORD", "")
    database_name = os.environ.get("PG_DB", "")
    database_schema = os.environ.get("PG_SCHEMA", "")
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}?options=-csearch_path%3D{database_schema}"


# Function to create query engine
def create_query_engine():
    db_engine = create_engine(get_database_uri())
    sql_database = SQLDatabase(db_engine)
    return NLSQLTableQueryEngine(sql_database)


# Main function to run the app
def main():
    st.title("Private Tex2SQL")
    initialize_settings()
    query_engine = create_query_engine()

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = query_engine.query(prompt)
                st.markdown("--------Response:--------")
                st.markdown(response)
                st.markdown("------AI generated SQL Query:-------")
                st.markdown(response.metadata["sql_query"])


if __name__ == "__main__":
    main()
