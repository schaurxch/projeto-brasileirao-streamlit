import streamlit as st
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter


# Função utilitária para carregar CSVs do KaggleHub
@st.cache_data
def load_csv_kaggle(file_path, drop_cols=None, rename_map=None):
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "adaoduque/campeonato-brasileiro-de-futebol",
        file_path  # agora argumento posicional
    )
    # remover colunas se existirem
    if drop_cols:
        for c in drop_cols:
            if c in df.columns:
                df.drop(columns=[c], inplace=True)
    # renomear se o nome antigo existir
    if rename_map:
        ren = {k: v for k, v in rename_map.items() if k in df.columns}
        if ren:
            df.rename(columns=ren, inplace=True)
    return df