from flask import Flask
from flask_cors import CORS

from backend.routes.gateway import gateway_bp
from backend.routes.auth import auth_bp


app = Flask(__name__)

CORS(app)

app.register_blueprint(
    gateway_bp,
    url_prefix="/v1"
)

app.register_blueprint(
    auth_bp,
    url_prefix="/v1/auth"
)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )