import pandas as pd
from pathlib import Path
from basedosdados import read_table


def save_table_parquet(
        dataset_id: str,
        table_id: str,
        billing_project_id: str = 'partos'
    ) -> str | None:
    savepath = f'{Path.home()}/Databases/basedosdados/{dataset_id}/{table_id}.parquet'
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