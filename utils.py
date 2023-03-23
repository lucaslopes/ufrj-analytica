from pathlib import Path


def get_table_path(
        table_id: str,
        dataset_id: str,
        origin: str = 'basedosdados',
        root_dir: str = 'Databases',
        file_ext: str = 'parquet',
    ) -> str:
    return f'{Path.home()}/{root_dir}/{origin}/{dataset_id}/{table_id}.{file_ext}'


####################################


def calc_bienio(x):
    if x % 2 == 0:
        bienio = f'{x}/{str(x+1)[-2:]}'
    else:
        bienio = f'{x-1}/{str(x)[-2:]}'
    return bienio

def calc_decada(x):
    decada = '2010-2014' if x < 2015 else '2015-2019'
    return decada