from flask import Flask

bruh = "hello, world. i'm python code"

# --------------------------------- FLASK SECTION ---------------------------------

app = Flask(__name__)

# Members API Route : pass data from backend to frontend
@app.route("/members")
def members():
    return {"members": ["Member1", bruh, "Member3"]}

if __name__ == "__main__":
    # switch to port 8000 for mac, because 5000 is taken by control centre
    app.run(port=8000, debug=True)