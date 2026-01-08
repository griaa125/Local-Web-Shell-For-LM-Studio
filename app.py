import re
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LM_API = "ВСТАВТЕ_СВОЙ_LM_API_СЮДА"
MODEL_NAME = "local-model"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"]

    r = requests.post(LM_API, json={
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты ChatGPT-подобный ассистент. "
                    "Размышления помещай внутрь <think>...</think>. "
                    "Пользователю показывай только финальный ответ."
                )
            },
            {"role": "user", "content": msg}
        ],
        "temperature": 0.7
    })

    raw = r.json()["choices"][0]["message"]["content"]

    # 🧠 извлекаем THINK
    think_match = re.search(r"<think>(.*?)</think>", raw, re.S)
    think = think_match.group(1).strip() if think_match else ""

    # 🧹 чистый финальный ответ
    answer = re.sub(r"<think>.*?</think>", "", raw, flags=re.S).strip()

    return jsonify({
        "answer": answer,
        "think": think
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)