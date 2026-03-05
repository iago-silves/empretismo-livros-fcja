document
  .getElementById("formUsuario")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const dados = {
      nome: document.querySelector("[name='nome']").value,
      email: document.querySelector("[name='email']").value,
      telefone: document.querySelector("[name='telefone']").value,
      endereco: document.querySelector("[name='endereco']").value,
    };

    try {
      const resposta = await fetch("/usuarios", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("Usuário cadastrado com sucesso!");
        window.location.href = "/listagem_usuarios.html";
      } else {
        alert(resultado.erro);
      }
    } catch (erro) {
      alert("Erro ao conectar com o servidor.");
    }
  });
