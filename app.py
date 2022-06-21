from fnmatch import translate
from flask import Flask, redirect, render_template, request, url_for
import requests
import os
from googletrans import Translator
app = Flask(__name__)
translater = Translator()

token = os.getenv("Bearer")

API_URL = os.getenv("API_URL")

token = "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"
API_URL = "https://api-inference.huggingface.co/models/Supreeth/Toxic-XLM_RoBERTa"

headers = {"Authorization": f"Bearer {token}"}


def checkAndTranslate(text):
    try:
        language = translater.detect(text)
        if language.lang != "hi":
            res = translater.translate(text, dest="hi", src=language.lang)
            return "success", res.text
        return text
    except Exception as e:
        return "error", text

# Analyse the sentence using api


def analyseText(text):
    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as e:
        return "error", str(e)

    if "error" in response.json():
        print(response.json())
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
    sentence = checkAndTranslate(sentence)
    if sentence[0] == "error":
        data["message"] = "Note:There was an error while translating your sentence, Prediction may not be accurate!!"
    result, score = analyseText(sentence[1])
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
