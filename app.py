import plotly.express as px
import geopandas as gpd
from pathlib import Path
import pandas as pd
import streamlit as st
from utils import get_table_path


st.title('Percentual de deslocamento de paturientes entre municípios')


@st.cache_data
def get_geo_by_scope(scope):
    scope_path = get_table_path('br_geobr_mapas', scope)
    df_scope = pd.read_parquet(scope_path)
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
        partos: str | list[str] = ['NOR', 'CES'],
    ):
    cols = ['id_municipio_6', f'id_{scope}', f'nome_{scope}']
    df = pd.merge(
        df_partos,
        df_mun[cols],
        left_on='origem',
        right_on='id_municipio_6',
        how='left')
    partos = [partos] if isinstance(partos, str) else partos
    df = df[df['parto'].isin(partos)]
    cols = ['ano', f'id_{scope}', f'nome_{scope}', 'deslocaram', 'total']
    df = df[cols].groupby(cols[:-2], as_index=False).sum()
    df['percentual'] = round(df['deslocaram'] / df['total'] * 100, 4)
    return df


@st.cache_data
def get_fig(df_mun, df_partos, scope):
    fig = px.choropleth_mapbox(
        select_df(df_mun, df_partos, scope),
        geojson=get_geo_by_scope(scope),
        locations=f'id_{scope}',
        hover_name = f'nome_{scope}',
        hover_data =[f'id_{scope}', f'nome_{scope}', 'deslocaram', 'total', 'percentual'],
        color="percentual",
        color_continuous_scale='ylorrd',
        range_color=(0, 100),
        mapbox_style="carto-positron",
        zoom=2,
        opacity=.75,
        center = {"lat": -15, "lon": -47},
        animation_frame="ano")
    return fig


@st.cache_data
def load_mun_and_partos():
    path_muns = get_table_path('br_bd_diretorios_brasil', 'municipio')
    partos_path = f'{Path.home()}/Databases/ufrj-analytica/partos.parquet'
    df_mun = pd.read_parquet(path_muns)
    df_partos = pd.read_parquet(partos_path)
    return df_mun, df_partos


scopes = [
    'municipio',
    'saude',
    'regiao_imediata',
    'regiao_intermediaria',
    'microrregiao',
    'mesorregiao',
    'uf',
    'regiao']
scope = st.sidebar.selectbox('Selecione o escopo', scopes, index=6)
# scope = scopes[-3]
df_mun, df_partos = load_mun_and_partos()
fig = get_fig(df_mun, df_partos, scope)
st.plotly_chart(fig)