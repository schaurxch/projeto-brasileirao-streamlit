import streamlit as st

def mostrar_elenco(team_id):
  st.markdown(f"""
    <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
    <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=1&matchesTab=0&teamLogo=1&statsTab=0" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
    </div>
    <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
    """, unsafe_allow_html=True)
  
def mostrar_estatisticas(team_id):
  st.markdown(f"""
    <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
    <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=0&matchesTab=0&teamLogo=1&statsTab=1" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
    </div>
    <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
    """, unsafe_allow_html=True)

def mostrar_proximos_jogos(team_id):
  st.markdown(f"""
    <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
    <iframe src="https://www.scoreaxis.com/widget/team-info/{team_id}?autoHeight=0&playersTab=0&matchesTab=1&teamLogo=1&statsTab=0" style="width:100%;height:350px;border:none;transition:all 300ms ease"></iframe>
    </div>
    <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Team data by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
      """, unsafe_allow_html=True)
  
def mostrar_tabela_atual():
  st.markdown("""
    <div style="border-width:1px;border-color:rgba(0, 0, 0, 0.15);border-style:solid;border-radius:8px;padding:10px;background:#fff;width:100%">
    <iframe src="https://www.scoreaxis.com/widget/standings-widget/648?autoHeight=0&teamsLogo=1&header=1&links=1" style="width:100%;height:550px;border:none;transition:all 300ms ease"></iframe>
    </div>
    <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left;">Data provided by <a target="_blank" href="https://www.scoreaxis.com/">Scoreaxis</a></div>
    """, unsafe_allow_html=True)
      