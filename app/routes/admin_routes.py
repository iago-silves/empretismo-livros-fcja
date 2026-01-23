from flask import Blueprint, request, jsonify
from app.services.administrador_service import AdministradorService

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/cadastro/admin", methods=["POST"])
def cadastrar_admin():
    data = request.json

    try:
        admin = AdministradorService.cadastrar_adm(
            nome=data["nome"],
            email=data["email"],
            senha=data["senha"]
        )

        return jsonify(admin), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
