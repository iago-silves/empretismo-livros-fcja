document.addEventListener("DOMContentLoaded", async function () {
  const select = document.getElementById("selectUsuario");

  try {
    const resposta = await fetch("/usuarios");
    const usuarios = await resposta.json();

    select.innerHTML = '<option value="">Selecione um usuário</option>';

    usuarios.forEach((usuario) => {
      const option = document.createElement("option");
      option.value = usuario.id;
      option.textContent = `${usuario.nome} (${usuario.email})`;
      select.appendChild(option);
    });
  } catch (erro) {
    select.innerHTML = '<option value="">Erro ao carregar usuários</option>';
  }
});

document
  .getElementById("formEmprestimo")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const dados = {
      usuario_id: parseInt(document.querySelector("[name='usuario_id']").value),
      autor: document.querySelector("[name='autor']").value,
      titulo: document.querySelector("[name='titulo']").value,
      editora: document.querySelector("[name='editora']").value,
      edicao: document.querySelector("[name='edicao']").value,
      ano: parseInt(document.querySelector("[name='ano']").value),
      local: document.querySelector("[name='local']").value,
      origem: document.querySelector("[name='origem']").value,
      observacao: document.querySelector("[name='observacao']").value,
      prazo_dias: parseInt(document.querySelector("[name='prazo_dias']").value),
    };

    try {
      const resposta = await fetch("/livros/emprestar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("Livro cadastrado e emprestado com sucesso!");
        window.location.href = "/usuarios";
      } else {
        alert(resultado.erro || "Erro ao registrar empréstimo");
      }
    } catch (erro) {
      alert("Erro ao conectar com o servidor.");
    }
  });
