from flask import Flask, send_from_directory
from models import db

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
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)
