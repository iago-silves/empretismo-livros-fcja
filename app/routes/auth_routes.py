from flask import Blueprint, request, jsonify
from app.services.administrador_service import AdministradorService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login/adm", methods=["POST"])
def login_administrador():
    data = request.json

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    admin = AdministradorService.autenticar_adm(email, senha)

    if not admin:
        return jsonify({"erro": "Credenciais inválidas"}), 401

    return jsonify({
        "id": admin.id,
        "nome": admin.nome,
        "email": admin.email
    }), 200
