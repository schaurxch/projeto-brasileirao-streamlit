import streamlit as st
from utils.db_utils import get_lista_times, get_ultimos_resultados, get_escudo_path, get_team_id
from pathlib import Path

ESCUDOS_PATH = Path("escudos")

def mostrar_home():
    st.title("Brasileirão 2025")
    times = get_lista_times()
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

        db_file = "data/brasileiro_2024.db"
        ultimos_resultados = get_ultimos_resultados(selected_time, db_file)

        # -----------------------------
        # 1️⃣ Últimos 5 resultados
        # -----------------------------
        #st.subheader("Últimos 5 Resultados (2024)")
        #for _, row in ultimos_resultados.iterrows():
            #if row['vencedor'] == selected_time:
                #emoji = "✅"
            #elif row['vencedor'] == "Empate":
                #emoji = "⚪"
            #else:
                #emoji = "❌"

            #partida_str = f"{row['mandante']} ({row['gols_mandante']}) x ({row['gols_visitante']}) {row['visitante']} - {row['data_partida']} {emoji}"
            #st.markdown(f"- {partida_str}")

        # -----------------------------
        # 2️⃣ Widgets dinâmicos (Scoreaxis) - altura fixa 350px
        # -----------------------------
        if team_id:
            # Elenco
            st.subheader("Informações do Time (Elenco)")
            st.markdown(f"""
            <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
                <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=1&matchesTab=0&teamLogo=1&statsTab=0" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
            </div>
            <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
            """, unsafe_allow_html=True)

            # Estatísticas
            st.subheader("Estatísticas da Equipe")
            st.markdown(f"""
            <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
                <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=0&matchesTab=0&teamLogo=1&statsTab=1" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
            </div>
            <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
            """, unsafe_allow_html=True)

            # Próximos jogos
            st.subheader("Próximas Partidas")
            st.markdown(f"""
            <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
                <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=0&matchesTab=1&teamLogo=1&statsTab=0" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
            </div>
            <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
            """, unsafe_allow_html=True)

        # -----------------------------
        # 3️⃣ Tabela atual do campeonato (fixa, altura 550px)
        # -----------------------------
        st.subheader("Tabela Atual")
        st.markdown("""
        <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
            <iframe src="https://www.scoreaxis.com/widget/standings-widget/648?autoHeight=0&teamsLogo=1&header=1&links=1" style="width:100%;height:550px;border:none;transition:all 300ms ease"></iframe>
        </div>
        <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Data provided by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
        """, unsafe_allow_html=True)
