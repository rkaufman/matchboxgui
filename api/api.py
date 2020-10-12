from flask import Flask, request, jsonify
from flask_cors import CORS
from .middlewares import login_required
import time

app = Flask(__name__)
CORS(app)

@app.route("/time", methods=["GET"])
@login_required
def get_current_time():
    return jsonify({"time": time.time()})