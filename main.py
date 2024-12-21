import os
import datetime
import csv
from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

signatures = {}
with open('signatures.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        lang = row["language"]
        del row["language"]
        signatures[lang] = row

def get_day():
    day = (datetime.date.today() - datetime.date(datetime.date.today().year, 1, 1)).days
    if not os.path.exists(f"wisdom/{day}"):
        day = 1
    return day

@app.route('/get_knowledge', methods=['GET'])
def get_knowledge():
    day = get_day()
    language = request.args.get('lang', 'en')
    if os.path.exists(f"wisdom/{day}/{language}.txt"):
        data = {}
        with open(f"wisdom/{day}/{language}.txt") as f:
            data["title"] = f.readline()
            f.readline() # skip
            data["date"] = f.readline()
            data["location"] = f.readline()
            f.readline() # skip
            data["knowledge"] = f.read()
        data["audio"] = f"/get_audio?lang={language}"
        data.update(signatures[language])
        return jsonify(data)
    return jsonify({"error": "Language not supported"}), 400

@app.route('/get_audio', methods=['GET'])
def get_audio():
    day = get_day()
    language = request.args.get('lang', 'en')
    if os.path.exists(f"wisdom/{day}/{language}.mp3"):
        return send_file(f"wisdom/{day}/{language}.mp3")
    return jsonify({"error": "Language not supported"}), 400

@app.route("/", methods=("GET","POST"))
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(
        port=int(os.environ.get("PORT", 8080))
    )
