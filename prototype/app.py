from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "study_data.json"

@app.route("/")
def index():
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
