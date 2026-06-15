from flask import Flask

from config.settings import (
    FLASK_SECRET_KEY
)

from routes.auth_routes import (
    auth_bp
)

from routes.dashboard_routes import (
    dashboard_bp
)
from routes.file_routes import (
    file_bp
)

app = Flask(__name__)

app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth_bp)

app.register_blueprint(
    dashboard_bp
)

app.register_blueprint(
    file_bp
)
@app.route("/")
def home():
    return "Document Platform Running v2"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
