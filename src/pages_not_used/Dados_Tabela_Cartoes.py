import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dados da Tabela Cartões", layout="wide")

st.title("Dados da Tabela Cartões :file_folder:")

tabela_cartoes = pd.read_csv("data/campeonato-brasileiro-cartoes.csv")
tabela_cartoes = tabela_cartoes.rename(columns={'rodata': 'rodada'})

# ---------- BOTÃO RESET ----------
if st.sidebar.button("🔄 Resetar Filtros"):
    st.session_state["colunas"] = list(tabela_cartoes.columns)
    st.session_state["rodada"] = list(tabela_cartoes['rodada'].unique())
    st.session_state["clube"] = list(tabela_cartoes['clube'].unique())
    st.session_state["jogador"] = list(tabela_cartoes['atleta'].unique())
    st.session_state["posicao"] = list(tabela_cartoes['posicao'].unique())
    st.session_state["camisa"] = list(tabela_cartoes['num_camisa'].dropna().unique())
    st.session_state["tipo"] = list(tabela_cartoes['cartao'].unique())
    st.session_state["minuto"] = list(tabela_cartoes['minuto'].unique())
    st.rerun()

with st.expander('Filtros das Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas', 
        options=list(tabela_cartoes.columns), 
        default=list(tabela_cartoes.columns),
        key="colunas"
    )

st.sidebar.header("Filtros")
with st.sidebar.expander("Rodada"):
    rodada = st.multiselect(
        "Selecione as Rodadas", 
        options=tabela_cartoes['rodada'].unique(), 
        default=list(tabela_cartoes['rodada'].unique()),
        key="rodada"
    )
with st.sidebar.expander("Clube"):
    clube = st.multiselect(
        "Selecione os Clubes", 
        options=tabela_cartoes['clube'].unique(), 
        default=list(tabela_cartoes['clube'].unique()),
        key="clube"
    )
with st.sidebar.expander("Jogador"):
    jogador = st.multiselect(
        "Selecione os Jogadores", 
        options=tabela_cartoes['atleta'].unique(), 
        default=list(tabela_cartoes['atleta'].unique()),
        key="jogador"
    )
with st.sidebar.expander("Posição do Jogador"):
    posicao = st.multiselect(
        "Selecione as Posições dos Jogadores", 
        options=tabela_cartoes['posicao'].unique(), 
        default=list(tabela_cartoes['posicao'].unique()),
        key="posicao"
    )
with st.sidebar.expander("Número da Camisa"):
    camisas_opcoes = tabela_cartoes['num_camisa'].dropna().unique()

    camisa = st.multiselect(
        "Selecione os Números das Camisas", 
        options=camisas_opcoes, 
        default=list(camisas_opcoes),  # agora só valores válidos
        key="camisa"
    )

with st.sidebar.expander("Tipo do Cartão"):
    tipo = st.multiselect(
        "Selecione os Tipos dos Cartões", 
        options=tabela_cartoes['cartao'].unique(), 
        default=list(tabela_cartoes['cartao'].unique()),
        key="tipo"
    )
with st.sidebar.expander("Minuto do Cartão"):
    minuto = st.multiselect(
        "Selecione os Minutos dos Cartões", 
        options=tabela_cartoes['minuto'].unique(), 
        default=list(tabela_cartoes['minuto'].unique()),
        key="minuto"
    )

query_tabela_cartoes_string = '''
rodada in @rodada and \
clube in @clube and \
atleta in @jogador and \
posicao in @posicao and \
num_camisa in @camisa and \
cartao in @tipo and \
minuto in @minuto
'''

tabela_cartoes_filtrada = tabela_cartoes.query(query_tabela_cartoes_string)
tabela_cartoes_filtrada = tabela_cartoes_filtrada[colunas]

st.dataframe(tabela_cartoes_filtrada)
st.markdown(f"A tabela possui {tabela_cartoes_filtrada.shape[0]} linhas e {tabela_cartoes_filtrada.shape[1]} colunas.")