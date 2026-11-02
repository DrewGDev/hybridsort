"""Interface Streamlit para explorar a lista e as estratégias de busca."""

from pathlib import Path
import sys
import time

import streamlit as st

# Permite executar este arquivo diretamente antes de instalar o pacote em modo editável.
SOURCE_DIRECTORY = Path(__file__).resolve().parents[1]
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from hybridsort.services.hybrid_list import HybridList


st.set_page_config(
    page_title="HybridSort | Busca híbrida",
    page_icon="🔎",
    layout="wide",
)

# Personaliza a aparência do Streamlit para deixar as áreas da aplicação
# visualmente mais organizadas sem alterar o comportamento dos componentes.
st.markdown(
    """
    <style>
    :root {
        --ink: #211c36;
        --muted: #77738b;
        --accent: #6758e8;
        --accent-dark: #5142cf;
        --surface: rgba(255, 255, 255, 0.92);
        --line: #e8e6f1;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 85% 0%, rgba(211, 205, 255, 0.32), transparent 34rem),
            linear-gradient(180deg, #f8f7fc 0%, #f2f3f9 100%);
        color: var(--ink);
        font-family: "Aptos", "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2.2rem;
        padding-bottom: 3.5rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #292344 0%, #352d5d 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f7f5ff;
    }

    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #d5d0ec;
    }

    section[data-testid="stSidebar"] input {
        color: #211c36 !important;
        background: #fff !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(255, 255, 255, 0.14);
    }

    .hero {
        position: relative;
        overflow: hidden;
        margin: 0 0 1.8rem;
        padding: 2rem 2.2rem;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 24px;
        background: linear-gradient(118deg, #302852 0%, #5144a2 52%, #7569ed 100%);
        box-shadow: 0 18px 44px rgba(66, 54, 137, 0.18);
        color: #fff;
    }

    .hero::after {
        position: absolute;
        top: -120px;
        right: -35px;
        width: 320px;
        height: 320px;
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 50%;
        box-shadow: 0 0 0 34px rgba(255, 255, 255, 0.035),
                    0 0 0 72px rgba(255, 255, 255, 0.025);
        content: "";
    }

    .hero-eyebrow {
        margin-bottom: 0.65rem;
        color: #dcd7ff;
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 0;
        color: #fff;
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 760;
        letter-spacing: -0.045em;
        line-height: 1.08;
    }

    .hero-copy {
        max-width: 700px;
        margin: 0.8rem 0 0;
        color: #eeecff;
        font-size: 1rem;
        line-height: 1.6;
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        margin-top: 1.15rem;
        padding: 0.45rem 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.24);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        color: #fff;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.07em;
    }

    h2, h3 {
        color: var(--ink);
        letter-spacing: -0.025em;
    }

    [data-testid="stForm"] {
        padding: 1.35rem 1.45rem 1.15rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: var(--surface);
        box-shadow: 0 9px 26px rgba(43, 36, 82, 0.055);
    }

    [data-testid="stForm"] h3 {
        margin-bottom: 0.9rem;
    }

    [data-testid="stWidgetLabel"] p {
        color: #59556d;
        font-weight: 600;
    }

    .stTextInput input, .stNumberInput input {
        border-radius: 10px;
    }

    .stButton button, [data-testid="stFormSubmitButton"] button {
        min-height: 2.7rem;
        border-radius: 10px;
        font-weight: 700;
        transition: transform 140ms ease, box-shadow 140ms ease;
    }

    .stButton button:hover, [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(81, 66, 207, 0.2);
    }

    [data-testid="stMetric"] {
        min-height: 112px;
        padding: 1rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: 0 7px 22px rgba(43, 36, 82, 0.045);
    }

    [data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 650;
    }

    [data-testid="stMetricValue"] {
        color: var(--ink);
        font-weight: 750;
    }

    [data-testid="stAlert"] {
        border-radius: 13px;
    }

    [data-testid="stProgress"] > div > div {
        border-radius: 999px;
    }

    .trace-card {
        padding: 1.25rem 1.4rem;
        border: 1px solid #e6e2f2;
        border-radius: 18px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f7ff 100%);
        box-shadow: 0 10px 28px rgba(43, 36, 82, 0.07);
        animation: trace-arrive 240ms ease-out;
    }

    .trace-card-top, .trace-labels, .trace-legend {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.65rem;
        flex-wrap: wrap;
    }

    .trace-card-top {
        margin-bottom: 0.9rem;
        color: #77738b;
        font-size: 0.78rem;
        font-weight: 650;
    }

    .trace-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: #efedff;
        color: #5142cf;
        font-weight: 750;
    }

    .trace-dot {
        width: 0.55rem;
        height: 0.55rem;
        border-radius: 50%;
        background: #6758e8;
        box-shadow: 0 0 0 4px rgba(103, 88, 232, 0.13);
        animation: trace-pulse 1.2s ease-in-out infinite;
    }

    .trace-card h4 {
        margin: 0.1rem 0 0.35rem;
        color: #211c36;
        font-size: 1.12rem;
    }

    .trace-card p {
        margin: 0 0 1rem;
        color: #68647b;
        line-height: 1.55;
    }

    .trace-stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.65rem;
        margin-bottom: 1.1rem;
    }

    .trace-stat {
        padding: 0.7rem 0.8rem;
        border: 1px solid #eeecf5;
        border-radius: 12px;
        background: #fff;
    }

    .trace-stat span {
        display: block;
        color: #77738b;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .trace-stat strong {
        display: block;
        margin-top: 0.2rem;
        color: #302852;
        font-size: 1rem;
    }

    .trace-labels {
        margin-bottom: 0.4rem;
        color: #77738b;
        font-size: 0.72rem;
        font-weight: 650;
    }

    .trace-rail {
        position: relative;
        height: 1rem;
        overflow: visible;
        border-radius: 999px;
        background: #e9e7f0;
    }

    .trace-active-range {
        position: absolute;
        top: 0;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #aaa0ff, #6758e8);
        transition: left 260ms ease, width 260ms ease;
    }

    .trace-midpoint {
        position: absolute;
        top: 50%;
        width: 1.05rem;
        height: 1.05rem;
        border: 3px solid #fff;
        border-radius: 50%;
        background: #332568;
        box-shadow: 0 2px 8px rgba(33, 28, 54, 0.32);
        transform: translate(-50%, -50%);
    }

    .trace-message {
        margin-top: 1rem;
        padding: 0.8rem 0.95rem;
        border-radius: 12px;
        font-weight: 700;
        line-height: 1.45;
    }

    .trace-message.is-left { background: #fff4df; color: #845719; }
    .trace-message.is-right { background: #eaf2ff; color: #345b9a; }
    .trace-message.is-found { background: #e4f6ee; color: #22734b; }

    .tail-track {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(78px, 1fr));
        gap: 0.55rem;
        margin: 0.9rem 0 0.7rem;
    }

    .tail-card {
        min-width: 0;
        padding: 0.7rem 0.45rem;
        border: 1px solid #e8e6f1;
        border-radius: 12px;
        background: #fff;
        text-align: center;
        transition: transform 180ms ease, background 180ms ease;
    }

    .tail-card small {
        display: block;
        color: #77738b;
        font-size: 0.66rem;
    }

    .tail-card strong {
        display: block;
        overflow-wrap: anywhere;
        color: #302852;
        font-size: 0.95rem;
    }

    .tail-card.visited { background: #f1f0f6; opacity: 0.72; }
    .tail-card.active {
        border-color: #7466ee;
        background: #efedff;
        box-shadow: 0 0 0 3px rgba(103, 88, 232, 0.12);
        transform: translateY(-3px);
    }
    .tail-card.found {
        border-color: #69bd91;
        background: #e4f6ee;
        box-shadow: 0 0 0 3px rgba(51, 151, 96, 0.11);
        transform: translateY(-3px);
    }

    .trace-legend {
        justify-content: flex-start;
        margin-top: 0.75rem;
        color: #77738b;
        font-size: 0.72rem;
    }

    .trace-legend span { display: inline-flex; align-items: center; gap: 0.35rem; }
    .legend-swatch { width: 0.65rem; height: 0.65rem; border-radius: 3px; background: #6758e8; }
    .legend-swatch.gray { background: #c9c6d3; }
    .legend-swatch.green { background: #58ad7d; }

    @keyframes trace-arrive {
        from { opacity: 0.35; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes trace-pulse {
        50% { box-shadow: 0 0 0 7px rgba(103, 88, 232, 0.05); }
    }

    [data-testid="stExpander"] {
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: 0 7px 22px rgba(43, 36, 82, 0.04);
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
    }

    hr {
        border-color: #e5e2ef;
    }

    @media (max-width: 700px) {
        .block-container { padding-top: 1.2rem; }
        .hero { padding: 1.5rem; border-radius: 18px; }
        [data-testid="stForm"] { padding: 1rem; }
        .trace-stats { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_search_step(
    step: dict[str, int | str],
    current_step: int,
    total_steps: int,
    key: int,
    ordered_region: list[int],
    tail: list[int],
) -> None:
    """Mostra uma comparação da busca com destaque visual e explicação simples."""
    if step["fase"] == "binaria":
        start = int(step["inicio"])
        end = int(step["fim"])
        middle = int(step["meio"])
        examined_value = int(step["valor"])
        decision = str(step["decisao"])
        candidates = end - start + 1
        list_size = max(len(ordered_region), 1)
        left_percent = start / list_size * 100
        range_percent = candidates / list_size * 100
        middle_percent = (middle + 0.5) / list_size * 100

        if decision == "encontrada":
            message_class = "is-found"
            explanation = (
                f"{examined_value} é igual à chave procurada. "
                f"Encontramos o valor no índice {middle}."
            )
        elif decision == "menor":
            message_class = "is-right"
            explanation = (
                f"{examined_value} é menor que {key}. "
                "Como a região está ordenada, descartamos o meio e tudo que está à esquerda."
            )
        else:
            message_class = "is-left"
            explanation = (
                f"{examined_value} é maior que {key}. "
                "Como a região está ordenada, descartamos o meio e tudo que está à direita."
            )

        st.markdown(
            f"""
            <div class="trace-card">
                <div class="trace-card-top">
                    <span class="trace-chip"><span class="trace-dot"></span>Busca binária · região ordenada</span>
                    <span>Etapa {current_step} de {total_steps}</span>
                </div>
                <h4>Compare o meio do intervalo com a chave</h4>
                <p>A busca binária reduz pela metade o trecho que ainda pode conter o valor.</p>
                <div class="trace-stats">
                    <div class="trace-stat"><span>Chave procurada</span><strong>{key}</strong></div>
                    <div class="trace-stat"><span>Valor no meio</span><strong>{examined_value}</strong></div>
                    <div class="trace-stat"><span>Candidatos neste passo</span><strong>{candidates:,}</strong></div>
                </div>
                <div class="trace-labels">
                    <span>Início: índice {start}</span>
                    <span>Meio: índice {middle}</span>
                    <span>Fim: índice {end}</span>
                </div>
                <div class="trace-rail">
                    <span class="trace-active-range" style="left:{left_percent:.4f}%; width:{range_percent:.4f}%"></span>
                    <span class="trace-midpoint" style="left:{middle_percent:.4f}%"></span>
                </div>
                <div class="trace-legend">
                    <span><i class="legend-swatch"></i>Intervalo ainda possível</span>
                    <span><i class="legend-swatch gray"></i>Parte já descartada</span>
                </div>
                <div class="trace-message {message_class}">{explanation}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    tail_index = int(step["indice"])
    examined_value = int(step["valor"])
    decision = str(step["decisao"])
    cards = []
    for index, value in enumerate(tail):
        if index == tail_index and decision == "encontrada":
            state_class = "found"
        elif index == tail_index:
            state_class = "active"
        elif index < tail_index:
            state_class = "visited"
        else:
            state_class = ""
        cards.append(
            f'<div class="tail-card {state_class}">'
            f'<small>Índice {len(ordered_region) + index}</small>'
            f'<strong>{value}</strong></div>'
        )

    if decision == "encontrada":
        message_class = "is-found"
        explanation = (
            f"A chave {key} foi encontrada no item {tail_index + 1} da cauda "
            f"(índice global {len(ordered_region) + tail_index})."
        )
    else:
        message_class = "is-right"
        explanation = (
            f"{examined_value} não é {key}. A cauda não está ordenada, "
            "então verificamos o próximo item, um por vez."
        )

    st.markdown(
        f"""
        <div class="trace-card">
            <div class="trace-card-top">
                <span class="trace-chip"><span class="trace-dot"></span>Busca sequencial · cauda</span>
                <span>Etapa {current_step} de {total_steps}</span>
            </div>
            <h4>Leia os itens da cauda em ordem de chegada</h4>
            <p>Como a cauda ainda não está ordenada, não podemos descartar metade dela.</p>
            <div class="trace-stats">
                <div class="trace-stat"><span>Chave procurada</span><strong>{key}</strong></div>
                <div class="trace-stat"><span>Item examinado</span><strong>{examined_value}</strong></div>
                <div class="trace-stat"><span>Posição na cauda</span><strong>{tail_index + 1} de {len(tail)}</strong></div>
            </div>
            <div class="tail-track">{''.join(cards)}</div>
            <div class="trace-legend">
                <span><i class="legend-swatch gray"></i>Já verificado</span>
                <span><i class="legend-swatch"></i>Comparação atual</span>
                <span><i class="legend-swatch green"></i>Chave encontrada</span>
            </div>
            <div class="trace-message {message_class}">{explanation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if "hybrid_list" not in st.session_state:
    st.session_state.hybrid_list = HybridList()
if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "insert_feedback" not in st.session_state:
    st.session_state.insert_feedback = None

with st.sidebar:
    st.title("⚙️ Configurações")
    seed = st.number_input(
        "Semente da lista inicial",
        value=42,
        step=1,
        help="Aplique uma semente diferente ao reiniciar a lista.",
    )

    if st.button("Reiniciar lista", type="secondary", width="stretch"):
        st.session_state.hybrid_list = HybridList(seed=int(seed))
        st.session_state.search_result = None
        st.session_state.search_animation_pending = False
        st.session_state.insert_feedback = None
        st.session_state.reset_notice = "Lista reiniciada com a semente selecionada."
        st.rerun()

    st.divider()
    st.subheader("Como funciona")
    st.markdown(
        """
        - **Região ordenada:** pesquisada por busca binária.
        - **Cauda:** recebe as novas chaves e é pesquisada em sequência.
        - Ao atingir o limite, a cauda é ordenada e incorporada à região principal.
        """
    )

lista: HybridList = st.session_state.hybrid_list
reset_notice = st.session_state.pop("reset_notice", None)

st.markdown(
    """
    <header class="hero">
        <div class="hero-eyebrow">Laboratório de algoritmos</div>
        <h1>HybridSort</h1>
        <p class="hero-copy">
            Explore como a busca binária percorre a região ordenada e como a
            busca sequencial encontra chaves recém-adicionadas na cauda.
        </p>
        <span class="hero-pill">BUSCA BINÁRIA&nbsp; · &nbsp;BUSCA SEQUENCIAL</span>
    </header>
    """,
    unsafe_allow_html=True,
)

if reset_notice:
    st.success(reset_notice)

search_column, insert_column = st.columns(2, gap="large")

with search_column:
    with st.form("search_form", border=True):
        st.subheader("Buscar uma chave")
        search_key = st.number_input(
            "Chave para procurar",
            value=lista.ordered_region[0],
            step=1,
            help="O valor inicial é uma chave existente. A busca tenta a região ordenada e depois a cauda.",
        )
        animate_search = st.checkbox(
            "Animar a busca passo a passo",
            value=True,
            help="Mostra cada comparação e como os candidatos diminuem.",
        )
        animation_delay = st.slider(
            "Tempo em cada etapa",
            min_value=0.05,
            max_value=0.7,
            value=0.25,
            step=0.05,
            format="%.2f s",
            help="Aumente o intervalo para explicar cada comparação durante a apresentação.",
        )
        search_submitted = st.form_submit_button("Buscar", type="primary")

with insert_column:
    with st.form("insert_form", clear_on_submit=True, border=True):
        st.subheader("Inserir uma chave")
        insert_key = st.number_input(
            "Nova chave",
            value=100_000,
            step=1,
            help="Chaves repetidas são rejeitadas. A nova chave entra na cauda.",
        )
        insert_submitted = st.form_submit_button("Adicionar à cauda")

if search_submitted:
    query = int(search_key)
    st.session_state.search_result = {
        "chave": query,
        **lista.search_key_with_trace(query),
        "animar": animate_search,
        "intervalo_animacao": animation_delay,
    }
    st.session_state.search_animation_pending = animate_search
    st.session_state.insert_feedback = None

if insert_submitted:
    value = int(insert_key)
    if lista.insert_key(value):
        st.session_state.insert_feedback = (
            "success",
            f"A chave {value} foi adicionada à cauda.",
        )
    else:
        st.session_state.insert_feedback = (
            "warning",
            f"A chave {value} já existe; a lista não foi alterada.",
        )
    # A inserção pode mudar os índices e o conteúdo, então o resultado anterior fica obsoleto.
    st.session_state.search_result = None
    st.session_state.search_animation_pending = False

if st.session_state.insert_feedback:
    feedback_type, feedback_message = st.session_state.insert_feedback
    getattr(st, feedback_type)(feedback_message)

result = st.session_state.search_result
if result:
    st.subheader("Resultado da busca")
    if result["encontrado"]:
        st.success(
            f"A chave {result['chave']} foi encontrada na região: {result['regiao']}."
        )
    else:
        st.warning(f"A chave {result['chave']} não foi encontrada na lista.")

    passos = result["passos"]
    if passos:
        st.markdown("#### Caminho percorrido")
        st.caption(
            "A animação mostra o valor comparado em cada etapa. Na região ordenada, "
            "a faixa roxa encolhe; na cauda, os itens são verificados em sequência."
        )

        if st.button(
            "Reproduzir percurso",
            key="replay_search_animation",
            help="Executa novamente as mesmas comparações, no ritmo escolhido acima.",
        ):
            st.session_state.search_animation_pending = True

        animation_slot = st.empty()
        animation_progress = st.progress(0, text="Preparando o percurso da busca...")
        animation_requested = st.session_state.get("search_animation_pending", False)

        if animation_requested:
            for numero_etapa, passo in enumerate(passos, start=1):
                animation_progress.progress(
                    numero_etapa / len(passos),
                    text=f"Etapa {numero_etapa} de {len(passos)}",
                )
                with animation_slot.container():
                    render_search_step(
                        passo,
                        numero_etapa,
                        len(passos),
                        int(result["chave"]),
                        lista.ordered_region,
                        lista.tail,
                    )
                time.sleep(float(result["intervalo_animacao"]))
            st.session_state.search_animation_pending = False
        else:
            animation_progress.progress(1, text="Busca concluída")
            with animation_slot.container():
                render_search_step(
                    passos[-1],
                    len(passos),
                    len(passos),
                    int(result["chave"]),
                    lista.ordered_region,
                    lista.tail,
                )

        linhas_do_rastro = []
        for numero_etapa, passo in enumerate(passos, start=1):
            if passo["fase"] == "binaria":
                decisao = str(passo["decisao"])
                valor = int(passo["valor"])
                alvo = int(result["chave"])
                if decisao == "encontrada":
                    explicacao = "Chave encontrada no meio do intervalo."
                elif decisao == "menor":
                    explicacao = f"{valor} < {alvo}: continuar à direita."
                else:
                    explicacao = f"{valor} > {alvo}: continuar à esquerda."
                intervalo = f"{passo['inicio']}–{passo['fim']}"
                indice_examinado = int(passo["meio"])
                estrategia = "Busca binária"
            else:
                valor = int(passo["valor"])
                decisao = str(passo["decisao"])
                explicacao = (
                    "Chave encontrada."
                    if decisao == "encontrada"
                    else "Valor diferente: avançar um item."
                )
                intervalo = f"Cauda · item {int(passo['indice']) + 1}"
                indice_examinado = len(lista.ordered_region) + int(passo["indice"])
                estrategia = "Busca sequencial"

            linhas_do_rastro.append(
                {
                    "Etapa": numero_etapa,
                    "Estratégia": estrategia,
                    "Intervalo antes da comparação": intervalo,
                    "Índice global examinado": indice_examinado,
                    "Valor examinado": valor,
                    "Decisão": explicacao,
                }
            )

        with st.expander("Ver todas as comparações", expanded=False):
            st.dataframe(
                linhas_do_rastro,
                width="stretch",
                hide_index=True,
            )

    binary_metric, sequential_metric, total_metric, index_metric = st.columns(4)
    binary_metric.metric("Iterações binárias", result["iteracoes_binarias"])
    sequential_metric.metric("Iterações sequenciais", result["iteracoes_sequenciais"])
    total_metric.metric("Total de iterações", result["total_iteracoes"])
    index_value = result["indice_global"]
    index_metric.metric(
        "Índice global (base 0)",
        index_value if index_value != -1 else "—",
    )

st.divider()
st.subheader("Visão geral da lista")

ordered_count = len(lista.ordered_region)
tail_count = len(lista.tail)
total_count = ordered_count + tail_count

ordered_metric, tail_metric, total_metric, remaining_metric = st.columns(4)
ordered_metric.metric("Região ordenada", ordered_count)
tail_metric.metric("Cauda atual", tail_count)
total_metric.metric("Total de chaves", total_count)
remaining_metric.metric(
    "Inserções até incorporar",
    HybridList.TAIL_LIMIT - tail_count,
)

st.progress(
    tail_count / HybridList.TAIL_LIMIT,
    text=f"Cauda: {tail_count} de {HybridList.TAIL_LIMIT} chaves acumuladas",
)

highlighted_index = (
    result["indice_global"]
    if result and result["encontrado"]
    else None
)
table_rows = []

for index, value in enumerate(lista.ordered_region):
    table_rows.append(
        {
            "Índice global": index,
            "Chave": value,
            "Região": "Ordenada",
            "Busca": "🔎 Encontrada" if index == highlighted_index else "",
        }
    )

for local_index, value in enumerate(lista.tail):
    global_index = ordered_count + local_index
    table_rows.append(
        {
            "Índice global": global_index,
            "Chave": value,
            "Região": "Cauda",
            "Busca": "🔎 Encontrada" if global_index == highlighted_index else "",
        }
    )

with st.expander(f"Visualizar as {total_count} chaves", expanded=True):
    st.dataframe(
        table_rows,
        width="stretch",
        height=460,
        hide_index=True,
        column_config={
            "Índice global": st.column_config.NumberColumn(
                help="Posição na lista completa, começando em zero."
            ),
            "Chave": st.column_config.NumberColumn(),
            "Região": st.column_config.TextColumn(),
            "Busca": st.column_config.TextColumn(),
        },
    )

st.caption(
    "Uma iteração conta um valor examinado no centro da busca binária ou um item "
    "percorrido na busca sequencial."
)
