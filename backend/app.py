from flask import Flask,render_template

import time

from config.settings import (
    FLASK_SECRET_KEY
)

from bootstrap.admin_initializer import (
    initialize_admin
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

from routes.admin_routes import (
    admin_bp
)

app = Flask(__name__)

app.secret_key = FLASK_SECRET_KEY

for attempt in range(3):
    try:
        initialize_admin()
        break

    except Exception as e:
        print(
            f"Admin initialization failed "
            f"(attempt {attempt + 1}/3): {e}"
        )

        time.sleep(5)

app.register_blueprint(auth_bp)

app.register_blueprint(
    dashboard_bp
)

app.register_blueprint(
    file_bp
)

app.register_blueprint(
    admin_bp
)

@app.route("/")
def home():
    return render_template(
        "landing.html"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
