from pathlib import Path
from typing import Any

import pandas as pd  # type: ignore

from repdata.cleanup import clean_dataframe  # or define locally
from repdata.config import get_sync_dir
from repdata.loader import load_tables
from repdata.logger import setup_logger

logger = setup_logger(__name__)


def clean_report_dict(d: dict[str, Any]) -> dict[str, Any]:
    return {
        key: (
            clean_dataframe(pd.DataFrame(val)).to_dict(orient="records")
            if isinstance(val, list)
            else clean_dataframe(pd.DataFrame([val])).iloc[0].to_dict()
        )
        for key, val in d.items()
    }


def filter_by_zakno(df: pd.DataFrame, column: str, zakno: int) -> pd.DataFrame:
    """Return a filtered DataFrame where `column` equals `zakno`."""
    return df.query(f"{column} == @zakno")


def build_report_dict(tables: dict[str, pd.DataFrame], zakno: int) -> dict[str, Any]:
    """Construct structured report dictionary for a given zakazka number."""
    zakazka = filter_by_zakno(tables["zakazky"], "z", zakno).squeeze()
    vzorky = filter_by_zakno(tables["vzorky"], "zak", zakno)
    objednavka = filter_by_zakno(tables["objednavky"], "zak", zakno)

    return {
        "zakazka": zakazka.to_dict(),
        "vzorky": vzorky.to_dict(orient="records"),
        "objednavka": objednavka.to_dict(orient="records"),
    }


def main(zakno: int) -> None:
    sync_dir: Path = get_sync_dir()
    logger.info(f"Using sync dir: {sync_dir}")
    tables = load_tables(sync_dir)

    raw = build_report_dict(tables, zakno)
    clean = clean_report_dict(raw)
    print(clean)


if __name__ == "__main__":
    main(zakno=2054)
