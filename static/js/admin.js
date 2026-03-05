document
  .getElementById("formCadastroAdmin")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const dados = {
      nome: document.querySelector("[name='nome']").value,
      email: document.querySelector("[name='email']").value,
      senha: document.querySelector("[name='senha']").value,
    };

    try {
      const resposta = await fetch("/adm/cadastro/admin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("Administrador cadastrado com sucesso!");
        window.location.href = "/login.html";
      } else {
        alert(resultado.erro);
      }
    } catch (erro) {
      alert("Erro ao conectar com o servidor.");
    }
  });
