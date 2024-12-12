import json
import os
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')

DATA_FILE = "survey_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    data = load_data()
    ip_address = request.remote_addr
    answers = {}
    yes_clicks = int(request.form.get('yes_clicks', 0))

    for key in request.form:
        if key != 'yes_clicks':
            answers[key] = request.form[key]

    if ip_address not in data:
        data[ip_address] = {"attempts": 0, "answers": [], "yes_clicks": 0}

    data[ip_address]["attempts"] += 1
    data[ip_address]["answers"].append(answers)
    data[ip_address]["yes_clicks"] = data[ip_address]["yes_clicks"] + yes_clicks #Суммируем

    save_data(data)
    return "Ответы сохранены. Спасибо!"

if __name__ == "__main__":
    app.run(debug=True)
