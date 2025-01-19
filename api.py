import requests
import os
from flask import Flask, jsonify

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GH_PAT")
REPO_OWNER = "kooroshkz"
REPO_NAME = "what_da_nerkh"

@app.route("/trigger-update")
def trigger_update():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.everest-preview+json"
    }
    data = {"event_type": "update_price"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        return jsonify({"message": "Update triggered successfully!"}), 200
    else:
        return jsonify({"error": "Failed to trigger update"}), 500

if __name__ == "__main__":
    app.run()
