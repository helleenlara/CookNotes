// Aguarda carregar a página
document.addEventListener('DOMContentLoaded', () => {
    console.log('%cCookNotes JS carregado!', 'color:#2E8B57; font-weight:bold;');

    iniciarAutoFecharAlertas();
    iniciarValidacaoSenhaTempoReal();
    iniciarBuscaInstantanea();
    iniciarAnimacoes();
});

// =====================================================================
// Auto fechar alertas
// =====================================================================
function iniciarAutoFecharAlertas() {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// =====================================================================
// Validação da senha em TEMPO REAL
// =====================================================================
function iniciarValidacaoSenhaTempoReal() {
    const senhaCampo = document.querySelector("#nova_senha") || document.querySelector("input[name='senha']");
    if (!senhaCampo) return;

    senhaCampo.addEventListener("input", () => {
        const senha = senhaCampo.value;

        validarRegra("regra-8", senha.length >= 8);
        validarRegra("regra-maiuscula", /[A-Z]/.test(senha));
        validarRegra("regra-minuscula", /[a-z]/.test(senha));
        validarRegra("regra-numero", /[0-9]/.test(senha));
        validarRegra("regra-especial", /[!@#$%^&*(),.?":{}|<>]/.test(senha));
    });
}

function validarRegra(id, condicao) {
    const item = document.getElementById(id);
    if (!item) return;

    if (condicao) {
        item.classList.add("valid");
        item.classList.remove("invalid");
    } else {
        item.classList.add("invalid");
        item.classList.remove("valid");
    }
}

// =====================================================================
// Modal estilizado de confirmação ao deletar
// =====================================================================
function confirmarDelecaoModal(nomeReceita, link) {
    const modalEl = document.getElementById("confirmDeleteModal");
    const modal = new bootstrap.Modal(modalEl);
    
    document.getElementById("deleteRecipeName").textContent = nomeReceita;
    document.getElementById("confirmDeleteButton").onclick = () => {
        window.location.href = link;
    };

    modal.show();
}

// =====================================================================
// Busca instantânea (sem reload)
// =====================================================================
function iniciarBuscaInstantanea() {
    const campoBusca = document.getElementById("busca-receitas");
    const cards = document.querySelectorAll(".card-receita");

    if (!campoBusca || cards.length === 0) return;

    campoBusca.addEventListener("input", () => {
        const filtro = campoBusca.value.toLowerCase();

        cards.forEach(card => {
            const nome = card.dataset.nome.toLowerCase();
            const categoria = card.dataset.categoria.toLowerCase();

            if (nome.includes(filtro) || categoria.includes(filtro)) {
                card.style.display = "block";
                card.classList.remove("fade-out");
                card.classList.add("fade-in");
            } else {
                card.classList.remove("fade-in");
                card.classList.add("fade-out");
                setTimeout(() => card.style.display = "none", 300);
            }
        });
    });
}

// =====================================================================
//  Animações suaves ao carregar
// =====================================================================
function iniciarAnimacoes() {
    const cards = document.querySelectorAll(".card");
    cards.forEach((card, i) => {
        setTimeout(() => {
            card.classList.add("animado");
        }, 100 * i);
    });
}


