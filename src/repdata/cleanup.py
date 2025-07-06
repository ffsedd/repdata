import pandas as pd  # type: ignore
from typing import Any


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Drop columns with all NaNs
    df = df.dropna(axis=1, how="all")

    # Strip whitespace and newlines from string entries
    df = df.map(
        lambda x: (
            x.strip().replace("\n", " ").replace("\r", "") if isinstance(x, str) else x
        )
    )

    # Convert "ano"/"ne" → True/False (optional and extendable)
    for col in df.select_dtypes(include="object"):
        if df[col].dropna().isin(["ano", "ne"]).all():
            df[col] = df[col].map({"ano": True, "ne": False})

    return df


def clean_report_dict(d: dict[str, Any]) -> dict[str, Any]:
    return {
        key: (
            clean_dataframe(pd.DataFrame(val)).to_dict(orient="records")
            if isinstance(val, list)
            else clean_dataframe(pd.DataFrame([val])).iloc[0].to_dict()
        )
        for key, val in d.items()
    }
