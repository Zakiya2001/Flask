from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    save_to_db(user_message)
    response = requests.post("http://localhost:5005/webhooks/rest/webhook",
                             json={"sender": "user", "message": user_message})
    messages = [msg.get("text") for msg in response.json()]
    return jsonify({"messages": messages})

def save_to_db(message):
    conn = sqlite3.connect("chatlog.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chatlog (message TEXT)")
    c.execute("INSERT INTO chatlog (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
