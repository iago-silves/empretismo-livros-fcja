from flask import Blueprint, request, jsonify
from app.services.administrador_service import AdministradorService

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")

@usuario_bp.route("", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()

    try:
        resultado = AdministradorService.cadastrar_usuario(
            nome=data["nome"],
            email=data["email"],
            telefone=data["telefone"],
            endereco=data["endereco"],
            setor=data["setor"],
            tipo= data["tipo"]
        )
        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@usuario_bp.route("/<email>", methods=["GET"])
def buscar_usuario(email):
    usuario = AdministradorService.buscar_usuario_por_email(email)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "telefone": usuario.telefone,
        "endereco": usuario.endereco,
        "setor": usuario.setor,
        "tipo": usuario.tipo,
        "bloqueado": usuario.bloqueado
    })

@usuario_bp.route("", methods=["GET"])
def listar_usuarios():
    usuarios = AdministradorService.listar_usuarios()

    return jsonify(usuarios), 200


@usuario_bp.route("/<email>/bloquear", methods=["PATCH"])
def bloquear_usuario(email):
    usuario = AdministradorService.buscar_usuario_por_email(email)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    AdministradorService.bloquear_usuario(usuario)

    return jsonify({"mensagem": "Usuário bloqueado"})


@usuario_bp.route("/<email>/desbloquear", methods=["PATCH"])
def desbloquear_usuario(email):
    usuario = AdministradorService.buscar_usuario_por_email(email)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    AdministradorService.desbloquear_usuario(usuario)

    return jsonify({"mensagem": "Usuário desbloqueado"})


@usuario_bp.route("/<email>/emprestimos-ativos", methods=["GET"])
def emprestimos_ativos(email):
    usuario = AdministradorService.buscar_usuario_por_email(email)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    quantidade = AdministradorService.quantidade_emprestimos_ativos(usuario)

    return jsonify({
        "usuario": usuario.email,
        "emprestimos_ativos": quantidade
    })


@usuario_bp.route("/emprestimos/<int:emprestimo_id>/devolucao", methods=["PATCH"])
def registrar_devolucao(emprestimo_id):

    emprestimo = AdministradorService.buscar_emprestimo_por_id(
        emprestimo_id
    )

    if not emprestimo:
        return jsonify({"erro": "Empréstimo não encontrado"}), 404

    AdministradorService.registrar_devolucao(emprestimo)

    return jsonify({"mensagem": "Devolução registrada"})


@usuario_bp.route("/emprestimos/<int:id>/renovar", methods=["PATCH"])
def renovar_emprestimo(id):
    try:
        dias = request.json.get("dias", 7)

        AdministradorService.renovar_emprestimo(id, dias)

        return jsonify({"mensagem": "Empréstimo renovado com sucesso"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        return jsonify({"erro": str(e)}), 400