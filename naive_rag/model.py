import chromadb
import logging


from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate
from llama_index.vector_stores.chroma import ChromaVectorStore

import logging

import sys
from os import path as osp

root = osp.abspath(osp.join(__file__, "../"))

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


global query_engine
query_engine = None


def init_llm():
    # llm = Ollama(model="llama2", request_timeout=300.0)
    # embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    llm = Ollama(model="llama3", request_timeout=300.0)
    embed_model = HuggingFaceEmbedding(model_name="nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    Settings.llm = llm
    Settings.embed_model = embed_model
    return Settings


def init_index(embed_model, input_dir):
    reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True)
    documents = reader.load_data()

    logging.info("index creating with `%d` documents", len(documents))

    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("naive_rag")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # use this to set custom chunk size and splitting
    # https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

    return index


def init_query_engine(index, topk=3):
    global query_engine

    # custome prompt template
    template = (
        "Here is some context related to the query:\n"
        "-----------------------------------------\n"
        "{context_str}\n"
        "-----------------------------------------\n"
        "Considering the above information, please respond to the following Question:\n"
        "{query_str}\n\n"
    )
    qa_template = PromptTemplate(template)

    # build query engine with custom template
    # text_qa_template specifies custom template
    # similarity_top_k configure the retriever to return the top 3 most similar documents,
    # the default value of similarity_top_k is 2
    query_engine = index.as_query_engine(text_qa_template=qa_template, similarity_top_k=topk)

    return query_engine


def chat(input_question, do_display=True):
    global query_engine

    response = query_engine.query(input_question)
    if do_display:
        display(response)
    return response.response


def chat_cmd(do_display=True):
    global query_engine

    while True:
        input_question = input("Enter your question (or 'exit' to quit): ")
        if input_question.lower() == "exit":
            break

        response = query_engine.query(input_question)
        if do_display:
            display(response)


def display(response):
    rag_str = ""
    sep = "+" * 100
    for i, source in enumerate(response.source_nodes):
        rag_str += f"Source No.{i}:\n{sep}\n" + source.text + f"\n{sep}\n"
    logging.info(f"Retrived text:\n{rag_str}")
    logging.info("Got response from llm:\n%s", response.response)


if __name__ == "__main__":
    Settings = init_llm()
    index = init_index(Settings.embed_model, osp.join(root, "docs"))
    init_query_engine(index, topk=3)
    chat_cmd()
