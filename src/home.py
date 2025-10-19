import streamlit as st
from utils.db_utils import get_lista_times, get_escudo_path, get_team_id
from services.service_scoreaxis import mostrar_elenco, mostrar_estatisticas, mostrar_proximos_jogos, mostrar_tabela_atual

def mostrar_home():
    st.title("Brasileirão 2025 :soccer:")
    times = get_lista_times()
    st.markdown(
    f'Obrigado [adaoduque](https://github.com/adaoduque) por disponibilizar os dados no '
    f'[Kaggle](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol/data) '
    f'e no [GitHub](https://github.com/adaoduque/Brasileirao_Dataset). '
    f'Um agradecimento especial ao [Scoreaxis](https://www.scoreaxis.com/) por fornecer os dados e widgets incorporáveis.'
    )
  
    st.subheader("Selecione um time:")

    cols = st.columns(5)
    selected_time = None
    for i, time in enumerate(times):
        with cols[i % 5]:
            st.image(get_escudo_path(time), width=60)
            if st.button(time):
                selected_time = time

    if selected_time:
        st.markdown(f"## {selected_time}")
        team_id = get_team_id(selected_time)

        if team_id:
            # Elenco
            st.subheader("Informações do Time (Elenco)")
            mostrar_elenco(team_id)

            # Estatísticas
            st.subheader("Estatísticas da Equipe")
            mostrar_estatisticas(team_id)

            # Próximos jogos
            st.subheader("Próximas Partidas")
            mostrar_proximos_jogos(team_id)

        # Tabela Atual
        st.subheader("Tabela Atual")
        mostrar_tabela_atual()
