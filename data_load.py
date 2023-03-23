import config
import plotly.express as px
import pandas as pd
from pathlib import Path
from basedosdados import read_table
from utils import get_table_path
import geopandas as gpd


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


def load_mun(df_mun, cols_muns=config.COLS_MUN):
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


def load_mun_and_partos():
    path_muns = get_table_path('br_bd_diretorios_brasil', 'municipio')
    partos_path = f'{Path.home()}/Databases/ufrj-analytica/partos.parquet'
    df_partos = pd.read_parquet(partos_path)
    df_mun = pd.read_parquet(path_muns)
    df_mun = load_mun(df_mun)
    return df_mun, df_partos


####################################


def save_table_parquet(
        dataset_id: str,
        table_id: str,
        billing_project_id: str = 'partos'
    ) -> str | None:
    savepath = get_table_path(dataset_id, table_id)
    if Path(savepath).exists():
        return savepath
    else:
        Path(savepath).parent.mkdir(parents=True, exist_ok=True)
    try:
        df = read_table(
            dataset_id=dataset_id,
            table_id=table_id,
            billing_project_id=billing_project_id)
        saved = df.to_parquet(savepath, index=False)
    except Exception as e:
        print(e)
        saved = False
    return savepath if saved else None


def save_list_tables(
        tables,
    ) -> dict:
    dict_log = dict()
    for dataset_id, table_id in tables:
        saved = save_table_parquet(
            dataset_id=dataset_id,
            table_id=table_id)
        dict_log[(dataset_id, table_id)] = saved
    return dict_log


def main():
    df_tables = pd.read_csv('tabelas.csv')
    tables = df_tables.to_numpy()
    return save_list_tables(tables)


__name__ == '__main__' and main()