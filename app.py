import streamlit as st
import config
from data_load import load_mun_and_partos, generate_figure

st.title(config.TITLE)

st.subheader(config.SUBTITLE)

type_parto = st.sidebar.multiselect(
    'Tipos de Parto',
    config.TYPES_PARTO,
    default=config.TYPES_PARTO[:2])

scope = st.sidebar.selectbox(
    'Resolução Geográfica',
    config.GEO_RESOLUTIONS,
    index=len(config.GEO_RESOLUTIONS) - 1)

time_step = st.sidebar.selectbox(
    'Intervalo de Tempo',
    config.TIME_INTERVAL,
    index=len(config.TIME_INTERVAL) - 1)

df_mun, df_partos = load_mun_and_partos()

st.plotly_chart(generate_figure(
    df_mun,
    df_partos,
    scope,
    time_step,
    type_parto))