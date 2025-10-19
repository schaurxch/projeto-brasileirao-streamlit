import streamlit as st
import pandas as pd
import plotly.express as px


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
st.markdown(f"A tabela possui :blue[{tabela_gols_filtrada.shape[0]}] linhas e :blue[{tabela_gols_filtrada.shape[1]}] colunas.")

agrupado_gols = tabela_gols_filtrada.groupby(["clube"]).size().reset_index(name="qtd_gols")
agrupado_gols = agrupado_gols.sort_values("qtd_gols", ascending=False)
agrupado_gols = agrupado_gols.head(10)

barra_gols = px.bar(
    agrupado_gols,
    x="clube",
    y="qtd_gols",
    title="Total de Gols por Clube (Top 10)",
    labels={"qtd_gols": "Quantidade de Gols", "clube": "Clube"},
    color="clube"  # opcional
)

agrupado_atletas = tabela_gols_filtrada.groupby(["atleta"]).size().reset_index(name="qtd_gols_atleta")
agrupado_atletas = agrupado_atletas.sort_values("qtd_gols_atleta", ascending=False)
agrupado_atletas = agrupado_atletas.head(10)

barra_atleta = px.bar(
    agrupado_atletas,
    x="atleta",
    y="qtd_gols_atleta",
    title="Total de Gols por Atleta (Top 10)",
    labels={"qtd_gols_atleta": "Quantidade de Gols", "atleta": "Atleta"},
    color="atleta" 
)



col1, col2 = st.columns(2, border=True)

with col1:
    st.plotly_chart(barra_gols)

with col2:
    st.plotly_chart(barra_atleta)