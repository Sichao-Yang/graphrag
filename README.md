this is a repo to test graphrag vs naive rag.

## graphRAG

follow [官方blog](https://microsoft.github.io/graphrag/) and [GraphRAG with Ollama](https://www.youtube.com/watch?v=6Yu6JpLMWVo&ab_channel=FahdMirza)

notice, you need to replace the embedding_model file in the graphrag lib (this is a hack).

also notice, for local rag, this hack will fail. so more modification needs to be done.

here is some cmds used:

```
conda create -n graphollama python=3.10 -y && conda activate graphollama

pip install ollama 

ollama pull mistral     # you need mistral to meet the context window limit
ollama pull nomic-embed-text 

pip install graphrag

mkdir -p ./graph_rag/input
cp book.txt graph_rag/input 

python3 -m graphrag.index --init --root ./graph_rag

cd graph_rag , vi settings
# change query model name, embedding model name, api_base
sudo find / -name openai_embeddings_llm.py

python3 -m graphrag.index --root /home/sichaoy/graphrag/tmp

python3 -m graphrag.query --root /home/sichaoy/graphrag/tmp --method global "What are the top themes in this story?"
```

## naiveRAG

follow [this](./naive_rag/README.md)