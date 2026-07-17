

# -----------------------------------------------------------
# O Meu Dia de Saúde - app para ajudar pessoas mais velhas
# a organizar a medicação e as consultas.
#
# Autor: Vasco Valente
# Para correr: streamlit run app.py
# -----------------------------------------------------------
 
import streamlit as st
from datetime import date, datetime
 
# ---------- Configuração da página ----------
st.set_page_config(page_title="O Meu Dia de Saúde", page_icon="💊", layout="centered")
 
# ---------- Letras grandes e botões grandes (CSS) ----------
# Este bloco só muda o TAMANHO das coisas, para ser fácil de ler.
st.markdown("""
<style>
    html, body, [class*="css"] { font-size: 22px; }
    h1 { font-size: 44px !important; }
    h2 { font-size: 34px !important; }
    .stButton button {
        font-size: 26px !important;
        padding: 18px 28px !important;
        border-radius: 14px !important;
        width: 100%;
    }
    .stCheckbox label p { font-size: 30px !important; font-weight: 600; }
    .stCheckbox label span { transform: scale(1.6); margin-right: 14px; }
    div[data-testid="stMetricValue"] { font-size: 40px !important; }
</style>
""", unsafe_allow_html=True)
 
# ---------- Memória da aplicação ----------
# Lista de medicamentos: nome, dose, hora do dia
if "medicamentos" not in st.session_state:
    st.session_state.medicamentos = [
        {"nome": "Ben-u-ron", "dose": "1 comprimido", "hora": "Pequeno-almoço"},
        {"nome": "Medicamento da tensão", "dose": "1 comprimido", "hora": "Almoço"},
        {"nome": "Vitamina D", "dose": "1 cápsula", "hora": "Jantar"},
    ]
 
# Lista de consultas: descrição e data
if "consultas" not in st.session_state:
    st.session_state.consultas = [
        {"descricao": "Consulta no médico de família", "data": date(2026, 7, 22)},
        {"descricao": "Análises ao sangue (em jejum!)", "data": date(2026, 7, 28)},
    ]
 
# Guarda quais os medicamentos já tomados HOJE.
# Se o dia mudar, a lista fica limpa outra vez.
hoje = date.today()
if st.session_state.get("dia_registado") != hoje:
    st.session_state.dia_registado = hoje
    st.session_state.tomados = set()
 
HORAS_DO_DIA = ["Pequeno-almoço", "Almoço", "Lanche", "Jantar", "Deitar"]
 
DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira",
               "quinta-feira", "sexta-feira", "sábado", "domingo"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
 
# ---------- Separadores: um para o dia a dia, outro para configurar ----------
aba_hoje, aba_gerir = st.tabs(["📅  O MEU DIA", "⚙️  Configurar (família)"])
 
# ============================================================
# ABA 1 - O MEU DIA (a parte simples, para a pessoa mais velha)
# ============================================================
with aba_hoje:
 
    # Data de hoje por extenso, bem grande
    dia_semana = DIAS_SEMANA[hoje.weekday()]
    hora_atual = datetime.now().hour
    if hora_atual < 12:
        st.title("Bom dia! ☀️")
    elif hora_atual < 20:
        st.title("Boa tarde! 🌤️")
    else:
        st.title("Boa noite! 🌙")
    st.header(f"Hoje é {dia_semana}, {hoje.day} de {MESES[hoje.month - 1]} de {hoje.year}")
    st.divider()
 
    # ----- Medicamentos de hoje -----
    st.header("💊 Os meus medicamentos de hoje")
 
    if not st.session_state.medicamentos:
        st.info("Não há medicamentos registados.")
    else:
        # Mostrar por ordem do dia: pequeno-almoço primeiro, deitar no fim
        for hora in HORAS_DO_DIA:
            meds_desta_hora = [m for m in st.session_state.medicamentos if m["hora"] == hora]
            if not meds_desta_hora:
                continue
            st.subheader(f"🕐 {hora}")
            for m in meds_desta_hora:
                # Cada medicamento é uma caixa para marcar "já tomei"
                chave = f"{m['nome']}-{m['hora']}"
                tomado = st.checkbox(
                    f"{m['nome']} — {m['dose']}",
                    value=(chave in st.session_state.tomados),
                    key="check-" + chave,
                )
                if tomado:
                    st.session_state.tomados.add(chave)
                    st.success("✅ Já tomou. Muito bem!")
                else:
                    st.session_state.tomados.discard(chave)
 
        # Resumo do dia
        total = len(st.session_state.medicamentos)
        feitos = len(st.session_state.tomados)
        st.divider()
        if feitos == total and total > 0:
            st.balloons()
            st.success(f"🎉 Parabéns! Tomou os {total} medicamentos de hoje.")
        else:
            st.warning(f"Faltam tomar {total - feitos} de {total} medicamentos.")
 
    st.divider()
 
    # ----- Próximas consultas -----
    st.header("🩺 As minhas próximas consultas")
 
    consultas_futuras = sorted(
        [c for c in st.session_state.consultas if c["data"] >= hoje],
        key=lambda c: c["data"],
    )
 
    if not consultas_futuras:
        st.info("Não tem consultas marcadas. 😊")
    else:
        for c in consultas_futuras:
            dias_que_faltam = (c["data"] - hoje).days
            data_bonita = f"{c['data'].day} de {MESES[c['data'].month - 1]}"
            if dias_que_faltam == 0:
                st.error(f"📌 **É HOJE!** — {c['descricao']}")
            elif dias_que_faltam == 1:
                st.warning(f"📌 **É AMANHÃ** — {c['descricao']}")
            else:
                st.info(f"📌 **{data_bonita}** (faltam {dias_que_faltam} dias) — {c['descricao']}")
 
    st.divider()
 
    # ----- Botão de ajuda -----
    st.header("📞 Precisa de ajuda?")
    st.link_button("Ligar ao Vasco — 913 302 230", "tel:913302230")
 
# ============================================================
# ABA 2 - CONFIGURAR (para um familiar preencher)
# ============================================================
with aba_gerir:
    st.title("⚙️ Configurar")
    st.write("Esta parte é para um familiar preencher os medicamentos e as consultas.")
 
    # Mostrar mensagem de sucesso da última ação (sobrevive ao redesenho)
    if "mensagem" in st.session_state:
        st.success(st.session_state.pop("mensagem"))
 
    # ----- Adicionar medicamento -----
    st.header("Adicionar medicamento")
    with st.form("novo_med", clear_on_submit=True):
        nome = st.text_input("Nome do medicamento", placeholder="ex.: Ben-u-ron")
        dose = st.text_input("Dose", placeholder="ex.: 1 comprimido")
        hora = st.selectbox("Quando tomar", HORAS_DO_DIA)
        if st.form_submit_button("➕ Adicionar medicamento"):
            if nome.strip():
                st.session_state.medicamentos.append(
                    {"nome": nome.strip(), "dose": dose.strip() or "1 comprimido", "hora": hora}
                )
                st.session_state.mensagem = f"'{nome}' adicionado!"
                st.rerun()  # redesenhar já, para aparecer na aba "O MEU DIA"
            else:
                st.error("Escreva o nome do medicamento.")
 
    # ----- Remover medicamento -----
    if st.session_state.medicamentos:
        st.header("Remover medicamento")
        nomes = [f"{m['nome']} ({m['hora']})" for m in st.session_state.medicamentos]
        escolhido = st.selectbox("Escolha o medicamento a remover", nomes)
        if st.button("🗑️ Remover este medicamento"):
            indice = nomes.index(escolhido)
            removido = st.session_state.medicamentos.pop(indice)
            st.success(f"'{removido['nome']}' removido.")
            st.rerun()
 
    st.divider()
 
    # ----- Adicionar consulta -----
    st.header("Adicionar consulta")
    with st.form("nova_consulta", clear_on_submit=True):
        descricao = st.text_input("Descrição", placeholder="ex.: Consulta de oftalmologia")
        data_consulta = st.date_input("Data da consulta", value=hoje, min_value=hoje)
        if st.form_submit_button("➕ Adicionar consulta"):
            if descricao.strip():
                st.session_state.consultas.append(
                    {"descricao": descricao.strip(), "data": data_consulta}
                )
                st.session_state.mensagem = "Consulta adicionada!"
                st.rerun()  # redesenhar já, para aparecer na aba "O MEU DIA"
            else:
                st.error("Escreva a descrição da consulta.")
 
    # ----- Remover consulta -----
    if st.session_state.consultas:
        st.header("Remover consulta")
        descricoes = [f"{c['descricao']} ({c['data']})" for c in st.session_state.consultas]
        escolhida = st.selectbox("Escolha a consulta a remover", descricoes)
        if st.button("🗑️ Remover esta consulta"):
            indice = descricoes.index(escolhida)
            st.session_state.consultas.pop(indice)
            st.success("Consulta removida.")
            st.rerun()
 
# ---------- Rodapé ----------
st.caption("Feito com carinho em Python e Streamlit · Vasco Valente")
 





