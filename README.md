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
cp fahd.txt graph_rag/input 

python3 -m graphrag.index --init --root ./graph_rag

cd graph_rag , vi settings
# change query model name, embedding model name, api_base
sudo find / -name openai_embeddings_llm.py

python3 -m graphrag.index --root ./graph_rag

python3 -m graphrag.query --root ./graph_rag --method global "What are the top themes in this story?"
```

example scripts:

```
#settings.yaml 

encoding_model: cl100k_base
skip_workflows: []
llm:
  api_key: ${GRAPHRAG_API_KEY}
  type: openai_chat # or azure_openai_chat
  model: mistral
  model_supports_json: true # recommended if this is available for your model.
  # max_tokens: 4000
  # request_timeout: 180.0
api_base: http://localhost:11434/v1
  # api_version: 2024-02-15-preview
  # organization: <organization_id>
  # deployment_name: <azure_model_deployment_name>
  # tokens_per_minute: 150_000 # set a leaky bucket throttle
  # requests_per_minute: 10_000 # set a leaky bucket throttle
  # max_retries: 10
  # max_retry_wait: 10.0
  # sleep_on_rate_limit_recommendation: true # whether to sleep when azure suggests wait-times
  # concurrent_requests: 25 # the number of parallel inflight requests that may be made

parallelization:
  stagger: 0.3
  # num_threads: 50 # the number of threads to use for parallel processing

async_mode: threaded # or asyncio

embeddings:
  ## parallelization: override the global parallelization settings for embeddings
  async_mode: threaded # or asyncio
  llm:
    api_key: ${GRAPHRAG_API_KEY}
    type: openai_embedding # or azure_openai_embedding
    model: nomic_embed_text
    api_base: http://localhost:11434/api
    # api_version: 2024-02-15-preview
```

```
#openai_embeddings_llm.py

from typing_extensions import Unpack
from graphrag.llm.base import BaseLLM
from graphrag.llm.types import (
    EmbeddingInput,
    EmbeddingOutput,
    LLMInput,
)
from .openai_configuration import OpenAIConfiguration
from .types import OpenAIClientTypes
import ollama

class OpenAIEmbeddingsLLM(BaseLLM[EmbeddingInput, EmbeddingOutput]):
    _client: OpenAIClientTypes
    _configuration: OpenAIConfiguration

    def __init__(self, client: OpenAIClientTypes, configuration: OpenAIConfiguration):
        self._client = client
        self._configuration = configuration

    async def _execute_llm(
        self, input: EmbeddingInput, **kwargs: Unpack[LLMInput]
    ) -> EmbeddingOutput | None:
        args = {
            "model": self._configuration.model,
            **(kwargs.get("model_parameters") or {}),
        }
        embedding_list = []
        for inp in input:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=inp)
            embedding_list.append(embedding["embedding"])
        return embedding_list
```

## naiveRAG

follow [this](./naive_rag/README.md)