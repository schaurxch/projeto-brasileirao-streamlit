import unicodedata
from pathlib import Path

# Lista fixa dos 20 times da Série A 2025
TIMES_SERIE_A_2025 = [
    "Botafogo", "Palmeiras", "Fortaleza", "Internacional", "Flamengo",
    "São Paulo", "Cruzeiro", "Bahia", "Corinthians", "Vitória",
    "Vasco", "Juventude", "Grêmio", "Fluminense", "Atlético-MG",
    "RB Bragantino", "Mirassol", "Ceará", "Sport", "Santos"
]

# IDs dos times no Scoreaxis
SCOREAXIS_IDS = {
    "Botafogo": 2864,
    "Palmeiras": 3422,
    "Fortaleza": 3621,
    "Internacional": 2696,
    "Flamengo": 1024,
    "São Paulo": 3496,
    "Cruzeiro": 3371,
    "Bahia": 692,
    "Corinthians": 303,
    "Vitória": 3440,
    "Vasco": 696,
    "Juventude": 48,
    "Grêmio": 2925,
    "Fluminense": 1095,
    "Atlético-MG": 3427,
    "RB Bragantino": 7808,
    "Mirassol": 11126,
    "Ceará": 12220,
    "Sport": 2352,
    "Santos": 3684
}

ESCUDOS_PATH = Path("assets")

def get_lista_times():
    return TIMES_SERIE_A_2025

def normalizar_nome_time(time: str) -> str:
    nome = time.lower()
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8')
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

def get_escudo_path(time: str) -> str:
    filename = f"{normalizar_nome_time(time)}.png"
    path = ESCUDOS_PATH / filename
    if path.exists():
        return str(path)
    return "https://via.placeholder.com/100?text=Escudo"

def get_team_id(time: str) -> int:
    #Retorna o ID do time no Scoreaxis
    return SCOREAXIS_IDS.get(time)
