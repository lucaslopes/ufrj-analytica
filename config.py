from pathlib import Path

PROJECT_ID = 'partos'

TITLE = 'Deslocamento de Gestantes entre Municípios no Brasil'

SUBTITLE = 'Análise do Acesso ao Parto Hospitalar pelo SUS na Década de 2010'

DESCRIPTION = 'Percentual de uma localidade é calculado por uma divisão, onde o numerador é a quantidade de procedimentos que realizaram o parto hospitalar em um município diferente ao de uma residência nessa localidade. E o denominador é a quantidade de procedimentos realizados que possuem residência nessa localidade.'

SIH_PATH = f'data/partos.parquet'

TYPES_PARTO = [
    'NOR', # Parto Normal 
    'CES', # Parto Cesariano 
    'NAR', # Parto Normal de Alto Risco
    'CAR', # Parto Cesariano de Alto Risco
    'NCT', # Parto Normal em Centro de Parto Normal
    'CLT'] # Parto Cesariano com Laqueadura Tubarina

TIME_INTERVAL = [
    'ano', # 2010, 2011, ..., 2018, 2019
    'bienio', # 2010/11, 2010/11, ..., 2018/19 
    'meia_decada'] # 2010-2014, 2015-2019

COLS_MUN = [ # Municípios
    'id_municipio_6', 'nome',
    'id_regiao_saude', 'nome_regiao_saude',
    'id_regiao_imediata', 'nome_regiao_imediata',
    'id_regiao_intermediaria', 'nome_regiao_intermediaria',
    'id_microrregiao', 'nome_microrregiao',
    'id_mesorregiao', 'nome_mesorregiao',
    'id_uf', 'sigla_uf', 'nome_uf',
    'nome_regiao']

GEO_RESOLUTIONS = [
    'municipio',
    'regiao_saude',
    'regiao_imediata',
    'regiao_intermediaria',
    'microrregiao',
    'mesorregiao',
    'uf',
    'regiao']

TABLES_TO_DOWNLOAD = [
    # (dataset_id, table_id),
    ('br_bd_diretorios_brasil','municipio'),
    ('br_geobr_mapas','municipio'),
    ('br_geobr_mapas','saude'),
    ('br_geobr_mapas','regiao_imediata'),
    ('br_geobr_mapas','regiao_intermediaria'),
    ('br_geobr_mapas','microrregiao'),
    ('br_geobr_mapas','mesorregiao'),
    ('br_geobr_mapas','uf'),
    ('br_geobr_mapas','regiao')]