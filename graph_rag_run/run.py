from os import path as osp
import os
from graphrag.index import cli

root_path = "/home/sichaoy/graphrag/example"


# ############ Step0: download source
# input_dir = osp.join(root_path, "input")
# os.makedirs(input_dir, exist_ok=True)
# import requests

# r = requests.get("https://www.gutenberg.org/cache/epub/24022/pg24022.txt")
# with open(osp.join(input_dir, "book.txt"), "w") as fp:
#     fp.write(r.text)


# ############ Step1: init settings.yaml
# cli.index_cli(
#     root=root_path,
#     verbose=True,
#     resume=None,
#     memprofile=False,
#     nocache=False,
#     reporter="print",
#     config=None,
#     emit="parquet,csv",
#     dryrun=False,
#     init=True,
#     overlay_defaults=False,
#     cli=True,
# )

# ############ Step2: modify settings.yaml
# import yaml

# setting_path = osp.join(root_path, "settings.yaml")
# with open(osp.join(root_path, "settings.yaml")) as stream:
#     try:
#         settings = yaml.safe_load(stream)
#     except yaml.YAMLError as exc:
#         print(exc)

# settings["llm"]["model"] = "mistral"
# settings["llm"]["api_base"] = "http://localhost:11434/v1"
# settings["embeddings"]["llm"]["model"] = "nomic_embed_text"
# settings["embeddings"]["llm"]["api_base"] = "http://localhost:11434/api"
# settings["chunks"]["size"] = 300

# # Write YAML file
# with open(setting_path, "w", encoding="utf8") as fp:
#     yaml.dump(settings, fp, default_flow_style=False, allow_unicode=True)


# ############ Step3: modify embedding file
# # the embedding model name is hardcoded in openai_embeddings_llm_replace.py with 'nomic_embed_text'
# src_file_path = "/home/sichaoy/graphrag/graph_rag/openai_embeddings_llm_replace.py"
# import sys

# for p in sys.path:
#     if "site-packages" in p:
#         break

# file_path = osp.join(p, "graphrag/llm/openai/openai_embeddings_llm.py")
# print(file_path)

# import shutil

# os.remove(file_path)
# shutil.copy(src=src_file_path, dst=file_path)


# ############ Step4: run indexing
# cli.index_cli(
#     root=root_path,
#     verbose=False,
#     resume=None,
#     memprofile=False,
#     nocache=False,
#     reporter=None,
#     config=None,
#     emit=None,
#     dryrun=False,
#     init=False,
#     overlay_defaults=False,
# )

# ############ Step5: run query
# from graphrag.query import cli

# query = "What are the top themes in this story?"
# cli.run_global_search(
#     data_dir=None,
#     root_dir=root_path,
#     community_level=2,
#     response_type="Multiple Paragraphs",
#     query=query,
# )
