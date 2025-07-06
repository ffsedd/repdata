import pandas as pd  # type: ignore


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
