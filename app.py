from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.admin_routes import admin_bp
from app.routes.usuarios_routes import usuario_bp
from app.routes.livros_routes import livro_bp
from flask import render_template

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(livro_bp)

    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/usuarios")
    def usuarios_page():
        return render_template("usuarios_listagem.html")
    
    @app.route("/adm/cadastro")
    def admin_page():
        return render_template("cadastro_admin.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )