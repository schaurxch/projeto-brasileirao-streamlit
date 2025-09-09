# main.py
import streamlit as st
from pages.home import mostrar_home

st.set_page_config(page_title="Brasileirão 2025", layout="wide")

mostrar_home()
