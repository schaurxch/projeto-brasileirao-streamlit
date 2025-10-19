import re
import streamlit as st
import pandas as pd
from services.service_kaggle import load_csv_kaggle
import plotly.express as px

st.set_page_config(page_title="Dados das Tabelas", layout="wide")
st.title("Dados das Tabelas :file_folder:")
st.markdown(
    f'Obrigado ao [adaoduque](https://github.com/adaoduque) por disponibilizar as tabelas (datasets) no '
    f'[Kaggle](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol/data) '
    f'e no [GitHub](https://github.com/adaoduque/Brasileirao_Dataset).'
)

tabela_gols_path = "campeonato-brasileiro-gols.csv"
tabela_cartoes_path = "campeonato-brasileiro-cartoes.csv"
tabela_full_path = "campeonato-brasileiro-full.csv"
tabela_estatisticas_path = "campeonato-brasileiro-estatisticas_full.csv"

rename_map={"rodata": "rodada"}

# Carregando as tabelas do Kaggle
#tabela_gols = load_csv_kaggle("campeonato-brasileiro-gols.csv", rename_map={"rodata": "rodada"})
#tabela_cartoes = load_csv_kaggle("campeonato-brasileiro-cartoes.csv", rename_map={"rodata": "rodada"})
#tabela_full = load_csv_kaggle("campeonato-brasileiro-full.csv", rename_map={"rodata": "rodada"})
#tabela_estatisticas = load_csv_kaggle("campeonato-brasileiro-estatisticas-full.csv", rename_map={"rodata": "rodada"})

# Seleção da tabela
st.selectbox(
    "Selecione a Tabela que Deseja Visualizar",
    options=["Selecione", "Tabela de Gols", "Tabela de Cartões", "Tabela Full", "Tabela de Estatísticas"],
    key="tabela_escolhida"
)
if st.session_state["tabela_escolhida"] == "Selecione":
    st.warning("Por favor, selecione uma tabela para visualizar os dados.")
    st.stop()
elif st.session_state["tabela_escolhida"] == "Tabela de Gols":
    tabela_gols = load_csv_kaggle(tabela_gols_path, rename_map=rename_map)
    tabela = tabela_gols
elif st.session_state["tabela_escolhida"] == "Tabela de Cartões":
    tabela_cartoes = load_csv_kaggle(tabela_cartoes_path, rename_map=rename_map)
    tabela = tabela_cartoes
elif st.session_state["tabela_escolhida"] == "Tabela Full":
    tabela_full = load_csv_kaggle(tabela_full_path, rename_map=rename_map)
    tabela = tabela_full
elif st.session_state["tabela_escolhida"] == "Tabela de Estatísticas":
    tabela_stats = load_csv_kaggle(tabela_estatisticas_path, rename_map=rename_map)
    tabela = tabela_stats
else:
    tabela = pd.DataFrame()  # fallback seguro

# Helper para transformar nomes de coluna em chaves seguras para session_state
def safe_key(col_name: str) -> str:
    return re.sub(r"\W+", "_", str(col_name)).strip("_")

# Cria os filtros dinamicamente na sidebar
for col in tabela.columns:
    safe = safe_key(col)
    unique_values = tabela[col].dropna().unique().tolist()
    # Tratamento especial para IDs
    if col in ("partida_id", "ID"):
        with st.sidebar.expander(f"Filtro: {col}"):
            id_val = st.number_input(
                f"Digite o valor de {col}",
                min_value=int(min(unique_values)) if len(unique_values) else 0,
                max_value=int(max(unique_values)) if len(unique_values) else 0,
                step=1,
                key=f"numinput_{safe}"
            )
            aplicar = st.button(f"Aplicar filtro de {col}", key=f"btn_{safe}")
            if aplicar:
                st.session_state[f"filtro_{safe}"] = [id_val]
            else:
                st.session_state.setdefault(f"filtro_{safe}", unique_values)
        continue
    # Tratamento especial para tempo
    if col.lower() == "data":
        with st.sidebar.expander(f"Filtro: {col}"):
            min_date, max_date = pd.to_datetime(min(unique_values)), pd.to_datetime(max(unique_values))
            faixa = st.date_input(
                f"Selecione o intervalo de {col}",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key=f"date_{safe}"
            )
            if isinstance(faixa, tuple) and len(faixa) == 2:
                start, end = faixa
                st.session_state[f"filtro_{safe}"] = tabela[
                    (pd.to_datetime(tabela[col]) >= pd.to_datetime(start)) &
                    (pd.to_datetime(tabela[col]) <= pd.to_datetime(end))
                ][col].unique().tolist()
        continue
    if col.lower() == "hora":
        with st.sidebar.expander(f"Filtro: {col}"):
            min_time = pd.to_datetime(min(unique_values)).time()
            max_time = pd.to_datetime(max(unique_values)).time()
            start = st.time_input("Hora inicial", value=min_time, key=f"time_start_{safe}")
            end = st.time_input("Hora final", value=max_time, key=f"time_end_{safe}")
            st.session_state[f"filtro_{safe}"] = tabela[
                (pd.to_datetime(tabela[col]).dt.time >= start) &
                (pd.to_datetime(tabela[col]).dt.time <= end)
            ][col].unique().tolist()
        continue
    # Filtros normais
    try:
        unique_sorted = sorted(unique_values, key=lambda x: str(x))
    except Exception:
        unique_sorted = unique_values

    with st.sidebar.expander(f"Filtro: {col}"):
        st.multiselect(
            f"Selecione os valores para {col}",
            options=unique_sorted,
            default=unique_sorted,
            key=f"filtro_{safe}"
        )

# Seleção de colunas a mostrar
with st.expander("Filtros das Colunas"):
    colunas = st.multiselect(
        "Selecione as Colunas",
        options=list(tabela.columns),
        default=list(tabela.columns),
        key="colunas"
    )

# Montagem dinâmica da query
query_parts = []
local_dict = {}

for i, col in enumerate(tabela.columns):
    safe = safe_key(col)
    key_name = f"filtro_{safe}"
    selected = st.session_state.get(key_name, None)

    if selected is None or len(selected) == 0:
        continue

    unique_values = tabela[col].dropna().unique().tolist()
    if set(map(str, selected)) == set(map(str, unique_values)):
        continue

    var_name = f"__var_{i}"
    local_dict[var_name] = selected
    col_quoted = col.replace("`", "")
    query_parts.append(f"`{col_quoted}` in @{var_name}")

query_string = " and ".join(query_parts)

# Aplicar filtros
if query_string:
    try:
        tabela_filtrada = tabela.query(query_string, local_dict=local_dict)
    except Exception as e:
        st.error(f"Erro ao aplicar filtros: {e}")
        tabela_filtrada = tabela.copy()
else:
    tabela_filtrada = tabela.copy()

# Botão de reset
if st.button("Resetar Filtros :arrows_counterclockwise:"):
    # Apagar apenas filtros dinâmicos
    for key in list(st.session_state.keys()):
        if key.startswith("filtro_") or key.startswith("numinput_") or key.startswith("date_") or key.startswith("time_"):
            del st.session_state[key]

    # Se quiser resetar também a seleção de colunas, precisa remover ANTES do multiselect ser renderizado
    if "colunas" in st.session_state:
        del st.session_state["colunas"]

    st.rerun()


# Exibir tabela filtrada
cols_to_show = st.session_state.get("colunas", list(tabela_filtrada.columns))
st.dataframe(tabela_filtrada[cols_to_show])
st.markdown(
    f"A tabela possui :blue[{tabela_filtrada.shape[0]}] linhas e :blue[{tabela_filtrada.shape[1]}] colunas."
)




