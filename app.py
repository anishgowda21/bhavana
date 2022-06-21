from flask import Flask, redirect, render_template, request, url_for
import requests
import os
app = Flask(__name__)


token = os.getenv("Bearer")

API_URL = os.getenv("API_URL")


headers = {"Authorization": f"Bearer {token}"}

# Analyse the sentence using api
token = "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"
API_URL = "https://api-inference.huggingface.co/models/Supreeth/Toxic-XLM_RoBERTa"


def analyseText(text):
    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as e:
        return "error", str(e)

    if "error" in response.json():
        return "error", "Model not loaded yet please wait for 15 seconds for the first time😊😊"
    else:
        data = response.json()[0]
        lab0 = data[0]["score"]
        lab1 = data[1]["score"]

        if lab0 > lab1:
            return "Angry", lab0
        elif lab1 > lab0:
            return "Not Angry", lab1
        else:
            return "Neutral", lab0


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html", data={})


@app.route("/analyse", methods=["GET"])
def analyse():
    data = {}
    sentence = request.args.get("inputText")
    if not sentence:
        data["result"] = "error"
        data["message"] = "Please enter a sentence to analyse"
        data["score"] = 0
        return render_template("home.html", data=data)
    result, score = analyseText(sentence)
    data["result"] = result

    if result == "error":
        data["message"] = score
        score = 0

    score = round(score*100, 2)
    data["score"] = score
    return render_template("home.html", data=data)


if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)
