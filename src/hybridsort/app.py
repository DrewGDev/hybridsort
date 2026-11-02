"""Interface Streamlit para explorar a lista e as estratégias de busca."""

from pathlib import Path
import sys

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
    }
    </style>
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
            value=0,
            step=1,
            help="A busca tenta primeiro a região ordenada e depois a cauda.",
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
        **lista.search_key(query),
    }
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
