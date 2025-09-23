import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dados da Tabela Full", layout="wide")

st.title("Dados da Tabela Full :file_folder:")

tabela_full = pd.read_csv("data/campeonato-brasileiro-full.csv")
tabela_full['data'] = pd.to_datetime(tabela_full['data'], format='%d/%m/%Y')
tabela_full = tabela_full.rename(columns={'rodata': 'rodada'})

# ---------- BOTÃO RESET ----------
if st.sidebar.button("🔄 Resetar Filtros"):
    st.session_state["colunas"] = list(tabela_full.columns)
    st.session_state["mandante"] = list(tabela_full['mandante'].unique())
    st.session_state["formacao_mandante"] = list(tabela_full['formacao_mandante'].unique())
    st.session_state["tecnico_mandante"] = list(tabela_full['tecnico_mandante'].unique())
    st.session_state["visitante"] = list(tabela_full['visitante'].unique())
    st.session_state["formacao_visitante"] = list(tabela_full['formacao_visitante'].unique())
    st.session_state["tecnico_visitante"] = list(tabela_full['tecnico_visitante'].unique())
    st.session_state["rodada"] = list(tabela_full['rodada'].unique())
    st.session_state["data"] = [tabela_full['data'].min(), tabela_full['data'].max()]
    st.session_state["arena"] = list(tabela_full['arena'].unique())
    st.session_state["estado_mandante"] = list(tabela_full['mandante_Estado'].unique())
    st.session_state["estado_visitante"] = list(tabela_full['visitante_Estado'].unique())
    st.rerun()
# ---------------------------------

with st.expander('Filtros das Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas', 
        options=list(tabela_full.columns), 
        default=list(tabela_full.columns),
        key="colunas"
    )

st.sidebar.header("Filtros")
with st.sidebar.expander("Mandantes"):
    mandante = st.multiselect("Selecione os Mandantes", 
                              options=tabela_full['mandante'].unique(), 
                              default=list(tabela_full['mandante'].unique()),
                              key="mandante")
with st.sidebar.expander("Formação dos Mandantes"):
    formacao_mandante = st.multiselect("Selecione as Formações dos Mandantes", 
                                       options=tabela_full['formacao_mandante'].unique(), 
                                       default=list(tabela_full['formacao_mandante'].unique()),
                                       key="formacao_mandante")
with st.sidebar.expander("Técnico dos Mandantes"):
    tecnico_mandante = st.multiselect("Selecione os Técnicos dos Mandantes", 
                                      options=tabela_full['tecnico_mandante'].unique(), 
                                      default=list(tabela_full['tecnico_mandante'].unique()),
                                      key="tecnico_mandante")
with st.sidebar.expander("Visitantes"):
    visitante = st.multiselect("Selecione os Visitantes", 
                               options=tabela_full['visitante'].unique(), 
                               default=list(tabela_full['visitante'].unique()),
                               key="visitante")  
with st.sidebar.expander("Formação dos Visitantes"):
    formacao_visitante = st.multiselect("Selecione as Formações dos Visitantes", 
                                        options=tabela_full['formacao_visitante'].unique(), 
                                        default=list(tabela_full['formacao_visitante'].unique()),
                                        key="formacao_visitante") 
with st.sidebar.expander("Técnico dos Visitantes"):
    tecnico_visitante = st.multiselect("Selecione os Técnicos dos Visitantes", 
                                       options=tabela_full['tecnico_visitante'].unique(), 
                                       default=list(tabela_full['tecnico_visitante'].unique()),
                                       key="tecnico_visitante")
with st.sidebar.expander("Rodadas"):
    rodada = st.multiselect("Selecione as Rodadas", 
                            options=tabela_full['rodada'].unique(), 
                            default=list(tabela_full['rodada'].unique()),
                            key="rodada")
with st.sidebar.expander("Data"):
    data = st.date_input("Selecione a Data", 
                         value=[tabela_full['data'].min(), tabela_full['data'].max()], 
                         min_value=tabela_full['data'].min(), 
                         max_value=tabela_full['data'].max(),
                         key="data")
with st.sidebar.expander("Arena"):
    arena = st.multiselect("Selecione as Arenas", 
                           options=tabela_full['arena'].unique(), 
                           default=list(tabela_full['arena'].unique()),
                           key="arena")
with st.sidebar.expander("Estado do Mandante"):
    estado_mandante = st.multiselect("Selecione os Estados dos Mandantes", 
                                     options=tabela_full['mandante_Estado'].unique(), 
                                     default=list(tabela_full['mandante_Estado'].unique()),
                                     key="estado_mandante")
with st.sidebar.expander("Estado do Visitante"):
    estado_visitante = st.multiselect("Selecione os Estados dos Visitantes", 
                                      options=tabela_full['visitante_Estado'].unique(), 
                                      default=list(tabela_full['visitante_Estado'].unique()),
                                      key="estado_visitante")

query_tabela_full_string = '''
    mandante in @mandante and \
    formacao_mandante in @formacao_mandante and \
    tecnico_mandante in @tecnico_mandante and \
    visitante in @visitante and \
    formacao_visitante in @formacao_visitante and \
    tecnico_visitante in @tecnico_visitante and \
    rodada in @rodada and \
    data >= @data[0] and data <= @data[1] and \
    arena in @arena and \
    mandante_Estado in @estado_mandante and \
    visitante_Estado in @estado_visitante
    '''
tabela_full_filtrada = tabela_full.query(query_tabela_full_string)
tabela_full_filtrada = tabela_full_filtrada[colunas]
    
st.dataframe(tabela_full_filtrada)

st.markdown(f"A tabela possui {tabela_full_filtrada.shape[0]} linhas e {tabela_full_filtrada.shape[1]} colunas.")
