from flask import Blueprint, request, jsonify
from app.services.administrador_service import AdministradorService

livro_bp = Blueprint("livros", __name__, url_prefix="/livros")


@livro_bp.route("/emprestar", methods=["POST"])
def autorizar_emprestimo():
    data = request.get_json()

    try:
        if not data:
            return jsonify({"erro": "JSON inválido ou ausente"}), 400

        usuario = AdministradorService.buscar_usuario_por_id(
            data["usuario_id"]
        )

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        resultado = AdministradorService.autorizar_emprestimo(
            usuario=usuario,
            autor=data["autor"],
            titulo=data["titulo"],
            editora=data["editora"],
            edicao=data["edicao"],
            ano=data["ano"],
            local=data["local"],
            origem=data["origem"],
            observacao=data.get("observacao"),
            prazo_dias=data["prazo_dias"]
        )

        return jsonify(resultado), 201

    except KeyError as e:
        return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500