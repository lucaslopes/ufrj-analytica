import plotly.express as px
import geopandas as gpd
from pathlib import Path
import pandas as pd
import streamlit as st
from utils import get_table_path


st.title('Percentual de deslocamento de paturientes entre municípios')


@st.cache_data
def get_geo_by_scope(scope):
    name = scope.split('_')[-1] if 'saude' in scope else scope
    scope_path = get_table_path('br_geobr_mapas', name)
    df_scope = pd.read_parquet(scope_path)
    if scope == 'municipio':
        df_scope['id_municipio'] = df_scope['id_municipio'].apply(
            lambda x: x[:-1])
    df_scope.set_index('id_' + scope, inplace=True)
    geo = gpd.GeoSeries.from_wkt(df_scope['geometria']) # convert the geo coordinates column to a GeoSeries
    geo.set_crs(epsg=4326, inplace=True) # project the GeoSeries to a common coordinate reference system
    geo = geo.to_crs(epsg=4326)
    return geo


@st.cache_data
def select_df(
        df_mun: pd.DataFrame,
        df_partos: pd.DataFrame,
        scope: str,
        time_step: str,
        partos: str | list[str] = ['NOR', 'CES'],
    ):
    cols = [f'id_{scope}', f'nome_{scope}']
    if scope != 'municipio':
        cols = ['id_municipio'] + cols
    df = pd.merge(
        df_partos,
        df_mun[cols],
        left_on='origem',
        right_on='id_municipio',
        how='left')
    partos = [partos] if isinstance(partos, str) else partos
    df = df[df['parto'].isin(partos)]
    if time_step == 'bienio':
        df[time_step] = df['ano'].apply(
            lambda x: f'{x}/{str(x+1)[-2:]}' if x % 2 == 0 else f'{x-1}/{str(x)[-2:]}')
    if time_step == 'meia_decada':
        df[time_step] = df['ano'].apply(
            lambda x: '2010-2014' if x < 2015 else '2015-2019')
    cols = [time_step, f'id_{scope}', f'nome_{scope}', 'deslocaram', 'total']
    df = df[cols].groupby(cols[:-2], as_index=False).sum()
    df['percentual'] = round(df['deslocaram'] / df['total'] * 100, 4)
    return df


@st.cache_data
def generate_figure(df_mun, df_partos, scope, time_step, type_parto):
    fig = px.choropleth_mapbox(
        select_df(df_mun, df_partos, scope, time_step, type_parto),
        geojson=get_geo_by_scope(scope),
        locations=f'id_{scope}',
        hover_name = f'nome_{scope}',
        hover_data =[f'id_{scope}', f'nome_{scope}', 'deslocaram', 'total', 'percentual'],
        color="percentual",
        color_continuous_scale='ylorrd',
        range_color=(0, 100),
        mapbox_style="carto-positron",
        zoom=2.6,
        opacity=.75,
        center = {"lat": -15, "lon": -55},
        animation_frame=time_step,
        width=700,
        height=600,)
    return fig


@st.cache_data
def load_mun_and_partos():
    path_muns = get_table_path('br_bd_diretorios_brasil', 'municipio')
    partos_path = f'{Path.home()}/Databases/ufrj-analytica/partos.parquet'
    df_mun = pd.read_parquet(path_muns)
    df_partos = pd.read_parquet(partos_path)
    return df_mun, df_partos


def load_mun(df_mun):
    cols_muns = [
        'id_municipio_6', 'nome',
        'id_regiao_saude', 'nome_regiao_saude',
        'id_regiao_imediata', 'nome_regiao_imediata',
        'id_regiao_intermediaria', 'nome_regiao_intermediaria',
        'id_microrregiao', 'nome_microrregiao',
        'id_mesorregiao', 'nome_mesorregiao',
        'id_uf', 'sigla_uf', 'nome_uf',
        'nome_regiao']
    df = df_mun[cols_muns].copy()
    df_regiao = pd.read_parquet(get_table_path('br_geobr_mapas', 'regiao'))
    df_regiao = df_regiao[['id_regiao', 'nome_regiao']]
    df = df.merge(df_regiao, on='nome_regiao', how='left')
    df.rename(columns={
        'nome': 'nome_municipio',
        'id_municipio_6': 'id_municipio',
    }, inplace=True)
    df['id_regiao'].fillna(5, inplace=True)
    return df


scopes = [
    'municipio',
    'regiao_saude',
    'regiao_imediata',
    'regiao_intermediaria',
    'microrregiao',
    'mesorregiao',
    'uf',
    'regiao']
type_parto = st.sidebar.multiselect('Selecione o tipo de parto', ['NOR', 'CES', 'NAR', 'CAR', 'NCT', 'CLT'], default=['NOR', 'CES'])
scope = st.sidebar.selectbox('Selecione o escopo de localidade', scopes, index=7)
time_step = st.sidebar.selectbox('Selecione o intervalo de tempo', ['ano', 'bienio', 'meia_decada'], index=2)
df_mun, df_partos = load_mun_and_partos()
df_mun = load_mun(df_mun)
fig = generate_figure(df_mun, df_partos, scope, time_step, type_parto)
st.plotly_chart(fig)