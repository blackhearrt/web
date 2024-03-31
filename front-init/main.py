from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import socket
import json
import os
from threading import Thread

app = Flask(__name__)


STORAGE_FOLDER = "storage"
DATA_FILE = os.path.join(STORAGE_FOLDER, "data.json")


def save_to_json(data):
    with open(DATA_FILE, "a") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        username = request.form["username"]
        message_text = request.form["message"]
        
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        
        data = {
            timestamp: {
                "username": username,
                "message": message_text
            }
        }
        
       
        send_to_socket(data)
        
        return redirect(url_for("index"))
    
    return render_template("message.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404

def send_to_socket(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(json.dumps(data).encode(), ("localhost", 5000))
    client_socket.close()

def handle_socket_data():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 5000))

    while True:
        data, addr = server_socket.recvfrom(1024)
        data = json.loads(data.decode())
        save_to_json(data)

    server_socket.close()

if __name__ == "__main__":
    if not os.path.exists(STORAGE_FOLDER):
        os.makedirs(STORAGE_FOLDER)

    socket_thread = Thread(target=handle_socket_data)
    socket_thread.daemon = True
    socket_thread.start()

    app.run(port=3000)
