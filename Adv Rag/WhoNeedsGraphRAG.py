import os
from llama_index import (
    VectorStoreIndex,
    KnowledgeGraphIndex,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
)
from llama_index.graph_stores import NebulaGraphStore
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import LangchainEmbedding
from llama_index.llms import LlamaCPP
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama


import spacy
import re
from collections import Counter

# Step 1: Build the Knowledge Graph 


space_name = "llamaindex"
edge_types = ["relationship"]
rel_prop_names = ["relationship"]
tags = ["entity"]

graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)

# Step 2: Build the Vector Store
import chromadb
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("guardians_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)


storage_context = StorageContext.from_defaults(
    graph_store=graph_store,
    vector_store=vector_store
)

# Step 3: Set up the Service Context and models
ollama_embed_model = LangchainEmbedding(
    OllamaEmbeddings(model="llama3")
)

ollama_llm = Ollama(model="llama3")

service_context = ServiceContext.from_defaults(
    llm=ollama_llm,
    embed_model=ollama_embed_model
)

# Step 4: Load data and create indices
from llama_index import download_loader
WikipediaReader = download_loader("WikipediaReader")
loader = WikipediaReader()
documents = loader.load_data(pages=['Guardians of the Galaxy Vol. 3'], auto_suggest=False)


kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=10,
    service_context=service_context,
    include_embeddings=True,
)


vector_index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    service_context=service_context,
)

# Save indices
kg_index.storage_context.persist(persist_dir="./storage/kg_index")
vector_index.storage_context.persist(persist_dir="./storage/vector_index")

# Step 5: Setting up the base for query using Knowledge Graph and Vector Store

from llama_index.query_engine import KnowledgeGraphQueryEngine
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine


kg_storage_context = StorageContext.from_defaults(persist_dir="./storage/kg_index")
vector_storage_context = StorageContext.from_defaults(persist_dir="./storage/vector_index")

kg_index = load_index_from_storage(storage_context=kg_storage_context)
vector_index = load_index_from_storage(storage_context=vector_storage_context)


kg_query_engine = KnowledgeGraphQueryEngine(
    index=kg_index,
    service_context=service_context,
    verbose=True,
)

vector_retriever = VectorIndexRetriever(index=vector_index)
vector_query_engine = RetrieverQueryEngine(
    retriever=vector_retriever,
    node_postprocessors=[],
    service_context=service_context
)


#Step 6: Define the functions to extract entities, query the knowledge graph, and generate the response ... to be continued, building own entities extraction algo from the kg to send it to the vector store
