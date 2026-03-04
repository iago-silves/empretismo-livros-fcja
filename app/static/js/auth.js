document
  .getElementById("formLogin")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const dados = {
      email: document.querySelector("[name='email']").value,
      senha: document.querySelector("[name='senha']").value,
    };

    try {
      const resposta = await fetch("/login/adm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("Login realizado com sucesso!");

        // Aqui você decide para onde ir após login
        window.location.href = "/admin/dashboard";
      } else {
        alert(resultado.erro);
      }
    } catch (erro) {
      alert("Erro ao conectar com o servidor.");
    }
  });
