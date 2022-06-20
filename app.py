from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)


token = os.getenv("Bearer")

API_URL = os.getenv("API_URL")
headers = {"Authorization": f"Bearer {token}"}

# Analyse the sentence using api


def analyseText(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if "error" in response.json():
        return "error", 0.0
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
    if request.method == "POST":
        sentence = request.form["inputText"]
        result = analyseText(sentence)
        print(result)
        return render_template("home.html", data={"result": result, "setence": sentence})

    return render_template("home.html", data={})


@app.route("/analyse", methods=["GET"])
def analyse():
    sentence = request.args.get("inputText")
    result, score = analyseText(sentence)
    score = round(score*100, 2)
    return render_template("home.html", data={"result": result, "sentence": sentence, "score": score})


if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)
