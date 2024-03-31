import json
from flask import Flask, request

bruh = "hello, world. i'm python code"
notes = []

# --------------------------------- FLASK SECTION ---------------------------------

app = Flask(__name__)

@app.route('/send-data', methods=['POST'])
def receive_data():
    global notes
    notes = request.json  # Get the JSON data from the request
    print("Received data:", notes)
    return "Data received successfully"

# Members API Route : pass data from backend to frontend
@app.route("/members")
def members():
    global notes
    print("members is membering!!!!")
    return notes

if __name__ == "__main__":
    # switch to port 8000 for mac, because 5000 is taken by control centre
    app.run(port=8000, debug=True)