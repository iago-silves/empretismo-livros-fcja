from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.admin_routes import admin_bp
from app.routes.usuarios_routes import usuario_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(usuario_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )