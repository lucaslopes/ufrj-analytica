
TITLE = 'Deslocamento de Gestantes entre Municípios no Brasil'

SUBTITLE = 'Análise do Acesso ao Parto Hospitalar pelo SUS na Década de 2010'

TYPES_PARTO = ['NOR', 'CES', 'NAR', 'CAR', 'NCT', 'CLT']

TIME_INTERVAL = ['ano', 'bienio', 'meia_decada']

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
