from pathlib import Path


def get_table_path(
        dataset_id: str,
        table_id: str,
    ) -> str:
    return f'{Path.home()}/Databases/basedosdados/{dataset_id}/{table_id}.parquet'
