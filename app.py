import os
import sys
import threading
import webbrowser
from flask import Flask, send_from_directory
from models import db

# 1. Handle paths for PyInstaller compression
if getattr(sys, 'frozen', False):
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, static_folder=static_folder)
else:
    app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carbon.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from routes.log import log_bp       
from routes.summary import summary_bp
app.register_blueprint(log_bp, url_prefix="/api")
app.register_blueprint(summary_bp, url_prefix="/api")

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 2. Auto-open the browser
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8000/')

if __name__ == "__main__":
    # Start the browser after a 1-second delay to ensure Flask is running
    threading.Timer(1.0, open_browser).start()
    app.run(port=8000)
