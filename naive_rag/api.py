from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import logging
import sys

import sys
from os import path as osp

root = osp.abspath(osp.join(__file__, "../"))
sys.path.append(root)

from model import init_llm, chat, init_index, init_query_engine
from config import *

app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

Settings = init_llm()
index = init_index(Settings.embed_model, osp.join(root, "docs"))
init_query_engine(index)


@app.route("/api/question", methods=["POST"])
def post_question():
    json = request.get_json(silent=True)
    question = json["question"]
    logging.info("User question: `%s`", question)

    resp = chat(question)
    data = {"answer": resp}

    return jsonify(data), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=HTTP_PORT, debug=True)
