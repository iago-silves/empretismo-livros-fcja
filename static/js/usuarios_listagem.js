document.addEventListener("DOMContentLoaded", async function () {
  try {
    const resposta = await fetch("/usuarios");

    const usuarios = await resposta.json();

    const tabela = document.getElementById("tabelaUsuarios");

    tabela.innerHTML = "";

    usuarios.forEach((usuario) => {
      const linha = document.createElement("tr");

      linha.innerHTML = `
        <td>${usuario.nome}</td>
        <td>${usuario.email}</td>
        <td>${usuario.telefone || ""}</td>
        <td>${usuario.tipo || ""}</td>
        <td>${usuario.setor || ""}</td>
        <td>
          <button onclick="editarUsuario(${usuario.id})">Editar</button>
          <button onclick="excluirUsuario(${usuario.id})">Excluir</button>
        </td>
      `;

      tabela.appendChild(linha);
    });
  } catch (erro) {
    console.error("Erro ao carregar usuários:", erro);
  }
});

function editarUsuario(id) {
  window.location.href = `/usuarios/editar/${id}`;
}

async function excluirUsuario(id) {
  if (!confirm("Deseja realmente excluir este usuário?")) return;

  try {
    const resposta = await fetch(`/usuarios/${id}`, {
      method: "DELETE",
    });

    if (resposta.ok) {
      alert("Usuário excluído com sucesso!");
      location.reload();
    } else {
      const erro = await resposta.json();
      alert(erro.erro);
    }
  } catch (erro) {
    alert("Erro ao excluir usuário.");
  }
}
