from flask import Flask, jsonify

app = Flask(__name__)

# Flag to control when the Raspberry Pi should perform the addition
task_trigger = {"perform_addition": False}


@app.route("/check", methods=["GET"])
def check():
    return jsonify(task_trigger)

@app.route("/trigger", methods=["POST"])
def trigger():
    print("triggered")

    task_trigger["perform_addition"] = True
    print(task_trigger)
    return jsonify({"message": "Addition task triggered!"}), 200

@app.route("/reset", methods=["POST"])
def reset():
    task_trigger["perform_addition"] = False
    return jsonify({"message": "Task reset!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
