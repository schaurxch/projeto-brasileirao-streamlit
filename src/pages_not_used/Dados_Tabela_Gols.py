import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dados da Tabela Gols", layout="wide")

st.title("Dados da Tabela Gols :file_folder:")

tabela_gols = pd.read_csv("data/campeonato-brasileiro-gols.csv")
tabela_gols = tabela_gols.rename(columns={'rodata': 'rodada'})

# ---------- BOTÃO RESET ----------
if st.sidebar.button("🔄 Resetar Filtros"):
    st.session_state["colunas"] = list(tabela_gols.columns)
    st.session_state["tempo"] = list(tabela_gols['rodada'].unique())
    st.session_state["clube"] = list(tabela_gols['clube'].unique())
    st.session_state["jogador"] = list(tabela_gols['atleta'].unique())
    st.session_state["tipo"] = list(tabela_gols['tipo_de_gol'].unique())
    st.session_state["minuto"] = list(tabela_gols['minuto'].unique())
    st.rerun()
# ---------------------------------

with st.expander('Filtros das Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas', 
        options=list(tabela_gols.columns), 
        default=list(tabela_gols.columns),
        key="colunas"
    )

st.sidebar.header("Filtros")

with st.sidebar.expander("Rodada"):
    tempo = st.multiselect(
        "Selecione os Tempos dos Gols", 
        options=tabela_gols['rodada'].unique(), 
        default=list(tabela_gols['rodada'].unique()),
        key="tempo"
    )
with st.sidebar.expander("Clube"):
    clube = st.multiselect(
        "Selecione os Clubes", 
        options=tabela_gols['clube'].unique(), 
        default=list(tabela_gols['clube'].unique()),
        key="clube"
    )
with st.sidebar.expander("Jogador"):
    jogador = st.multiselect(
        "Selecione os Jogadores", 
        options=tabela_gols['atleta'].unique(), 
        default=list(tabela_gols['atleta'].unique()),
        key="jogador"
    )
with st.sidebar.expander("Tipo do Gol"):
    tipo = st.multiselect(
        "Selecione os Tipos dos Gols", 
        options=tabela_gols['tipo_de_gol'].unique(), 
        default=list(tabela_gols['tipo_de_gol'].unique()),
        key="tipo"
    )
with st.sidebar.expander("Minuto do Gol"):
    minuto = st.multiselect(
        "Selecione os Minutos dos Gols", 
        options=tabela_gols['minuto'].unique(), 
        default=list(tabela_gols['minuto'].unique()),
        key="minuto"
    )

query_tabela_gols_string = '''
rodada in @tempo and \
clube in @clube and \
atleta in @jogador and \
tipo_de_gol in @tipo and \
minuto in @minuto
'''

tabela_gols_filtrada = tabela_gols.query(query_tabela_gols_string)
tabela_gols_filtrada = tabela_gols_filtrada[colunas]

st.dataframe(tabela_gols_filtrada)
st.markdown(f"A tabela possui {tabela_gols_filtrada.shape[0]} linhas e {tabela_gols_filtrada.shape[1]} colunas.")
