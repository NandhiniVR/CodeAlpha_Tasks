from flask import Flask, render_template, request, jsonify
from chatbot import generate_recommendation

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_bot_response():
    age        = request.form.get("age")
    gender     = request.form.get("gender")
    occasion   = request.form.get("occasion")
    theme      = request.form.get("theme")
    complexity = request.form.get("complexity")
    nationality = request.form.get("nationality")

    if occasion and occasion.lower() == "wedding":
        result = generate_recommendation(age, gender, occasion, theme, complexity, nationality)
    else:
        result = generate_recommendation(age, gender, occasion, theme, complexity, None)

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
