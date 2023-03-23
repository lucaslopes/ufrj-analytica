import config
import pandas as pd
from pathlib import Path


def load_sih(
        pcdas: bool = True
    ):
    try:
        df_sih = pd.read_parquet(config.SIH_PATH)
    except FileNotFoundError:
        sih_file = 'sih_pcdas' if pcdas else 'sih'
        sih_path: str = f'{Path.home()}/Databases/partos/{sih_file}.parquet'
        df_sih = pd.read_parquet(sih_path)
    return df_sih


def desl_per_ref(
        df: pd.DataFrame,
        ref: str = 'origem',
    ) -> pd.DataFrame:
    df_ref = df.copy()
    df_ref['deslocou'] = df_ref['origem'] != df_ref['destino']
    cols = [ref, 'ano', 'parto', 'deslocou']
    df_ref = df_ref[cols]
    df_ref['procedimentos'] = 1
    df_ref = df_ref.groupby(cols, as_index=False).sum()
    df_ref = df_ref.sort_values(by=cols).reset_index(drop=True)
    return df_ref


def group_all_cases(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
    df_all = df.drop('deslocou', axis=1)
    group_cols = list(df_all.columns[:3])
    df_all = df_all.groupby(
        by=group_cols, as_index=False).sum()
    df_all = df_all.sort_values(
        by=group_cols).reset_index(drop=True)
    df_all.rename(columns={
        'procedimentos': 'total'}, inplace=True)
    return df_all


def only_desl(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
    df_desl = df[df['deslocou'] == True].copy()
    df_desl = df_desl.drop('deslocou', axis=1)
    df_desl.rename(columns={
        'procedimentos': 'deslocaram'}, inplace=True)
    return df_desl


def merge_cases(
        df_all: pd.DataFrame,
        df_desl: pd.DataFrame,
    ) -> pd.DataFrame:
    group_cols = list(df_all.columns[:3])
    df_merge = df_all.merge(
        df_desl, on=group_cols, how='left')
    df_merge['deslocaram'].fillna(0, inplace=True)
    return df_merge


def main():
    df_sih = load_sih()
    df_ref = desl_per_ref(df_sih)
    df_all = group_all_cases(df_ref)
    df_desl = only_desl(df_ref)
    df_merge = merge_cases(df_all, df_desl)
    output_path = config.SIH_PATH # f'{Path.home()}/Databases/ufrj-analytica/partos.parquet'
    if not Path(output_path).exists():
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_merge.to_parquet(output_path, index=False)


__name__ == '__main__' and main()