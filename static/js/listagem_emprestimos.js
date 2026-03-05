document.addEventListener("DOMContentLoaded", carregarEmprestimos);

async function carregarEmprestimos() {
  const tbody = document.querySelector("#tabelaEmprestimos tbody");

  try {
    const resposta = await fetch("/usuarios/emprestimos");
    const emprestimos = await resposta.json();

    tbody.innerHTML = "";

    if (emprestimos.length === 0) {
      tbody.innerHTML =
        "<tr><td colspan='7'>Nenhum empréstimo encontrado</td></tr>";
      return;
    }

    emprestimos.forEach((emp) => {
      const linha = document.createElement("tr");
      const dataEmprestimo = new Date(emp.data_emprestimo);
      const hoje = new Date();
      const prazoFinal = new Date(dataEmprestimo);
      prazoFinal.setDate(prazoFinal.getDate() + emp.prazo_dias);

      let statusTexto = "";
      let statusClasse = "";

      if (emp.status === "devolvido") {
        statusTexto = "Devolvido";
        statusClasse = "status-devolvido";
      } else if (hoje > prazoFinal) {
        statusTexto = "Atrasado";
        statusClasse = "status-atrasado";
      } else {
        statusTexto = "Ativo";
        statusClasse = "status-ativo";
      }
      const botoes =
        emp.status === "devolvido"
          ? "-"
          : `
            <button onclick="renovar(${emp.id})">Renovar</button>
            <button onclick="devolver(${emp.id})">Devolver</button>
          `;

      linha.innerHTML = `
        <td>${emp.id}</td>
        <td>${emp.usuario_nome}</td>
        <td>${emp.titulo}</td>
        <td>${emp.data_emprestimo}</td>
        <td>${emp.prazo_dias} dias</td>
        <td class="${statusClasse}">${statusTexto}</td>
        <td>${botoes}</td>
      `;

      tbody.appendChild(linha);
    });
  } catch (erro) {
    tbody.innerHTML =
      "<tr><td colspan='7'>Erro ao carregar empréstimos</td></tr>";
  }
}

async function renovar(id) {
  const dias = prompt("Quantos dias deseja renovar?");

  if (!dias) return;

  try {
    const resposta = await fetch(`/usuarios/emprestimos/${id}/renovar`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dias: parseInt(dias) }),
    });

    if (resposta.ok) {
      alert("Empréstimo renovado!");
      carregarEmprestimos();
    } else {
      const erro = await resposta.json();
      alert(erro.erro || "Erro ao renovar");
    }
  } catch (erro) {
    alert("Erro ao conectar com o servidor.");
  }
}

async function devolver(id) {
  const confirmar = confirm("Deseja realmente registrar a devolução?");

  if (!confirmar) return;

  try {
    const resposta = await fetch(`/usuarios/emprestimos/${id}/devolucao`, {
      method: "PATCH",
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
      alert("Devolução registrada com sucesso!");
      carregarEmprestimos();
    } else {
      alert(resultado.erro || "Erro ao registrar devolução");
    }
  } catch (erro) {
    alert("Erro ao conectar com o servidor.");
  }
}
