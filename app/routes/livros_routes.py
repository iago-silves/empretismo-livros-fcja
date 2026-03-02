from flask import Blueprint, request, jsonify
from app.services.administrador_service import AdministradorService

livro_bp = Blueprint("livros", __name__, url_prefix="/livros")


@livro_bp.route("", methods=["POST"])
def cadastrar_livro():
    data = request.get_json()

    try:
        resultado = AdministradorService.cadastrar_livro(
            autor=data["autor"],
            titulo=data["titulo"],
            editora=data["editora"],
            edicao=data["edicao"],
            ano=data["ano"],
            local=data["local"],
            origem=data["origem"],
            observacao=data.get("observacao")
        )

        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@livro_bp.route("/<int:livro_id>", methods=["GET"])
def buscar_livro(livro_id):

    livro = AdministradorService.buscar_livro_por_id(livro_id)

    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    return jsonify({
        "id": livro.id,
        "autor": livro.autor,
        "titulo": livro.titulo,
        "editora": livro.editora,
        "edicao": livro.edicao,
        "ano": livro.ano,
        "local": livro.local,
        "origem": livro.origem,
        "observacao": livro.observacao
    })