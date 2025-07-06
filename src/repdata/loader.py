# src/reptexdata/loader.py
from pathlib import Path

import pandas as pd  # type: ignore

from repdata.config import get_sync_dir
from repdata.logger import setup_logger


logger = setup_logger(__name__)


def load_table(name: str, dpath: Path) -> pd.DataFrame:

    fpath = dpath / f"{name}.tsv"
    logger.info(f"Loading {fpath}")
    df = pd.read_csv(fpath, sep="\t", dtype={0: "Int64"}, skiprows=1)  # nullable int
    return df


def load_tables(dpath: Path) -> dict[str, pd.DataFrame]:
    return {
        "zakazky": load_table("zakazky", dpath),
        "vzorky": load_table("vzorky", dpath),
        "objednavky": load_table("objednavky", dpath),
    }


if __name__ == "__main__":
    sync_dir = get_sync_dir()
    logger.info(sync_dir)
    tables = load_tables(sync_dir)
    print(tables)
