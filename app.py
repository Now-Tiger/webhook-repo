from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
database_name = os.environ.get("DB_NAME", "")
db = client[database_name]
events_collection = db["events"]


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    event_data = None

    if event_type == "push":
        event_data = {
            "author": payload["pusher"]["name"],
            "action": "push",
            "to_branch": payload["ref"].split("/")[-1],
            "from_branch": None,
            "timestamp": datetime.utcnow(),
        }

    elif event_type == "pull_request":
        if payload["action"] == "closed" and payload["pull_request"].get("merged"):
            # Merge action
            event_data = {
                "author": payload["pull_request"]["user"]["login"],
                "action": "merge",
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow(),
            }
        elif payload["action"] == "opened":
            # Pull request action
            event_data = {
                "author": payload["pull_request"]["user"]["login"],
                "action": "pull_request",
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow(),
            }

    if event_data:
        events_collection.insert_one(event_data)
        return jsonify({"status": "success"}), 200

    return jsonify({"status": "ignored"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find().sort("timestamp", -1).limit(20))
    for event in events:
        event["_id"] = str(event["_id"])
        event["timestamp"] = event["timestamp"].isoformat()
    return jsonify(events)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
