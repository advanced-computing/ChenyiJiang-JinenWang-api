import pandas as pd


def clean_gender(genders: pd.Series) -> pd.Series:
    return genders.str.upper().str.strip()


def parse_posted_date(dates: pd.Series) -> pd.Series:
    return pd.to_datetime(dates, errors="coerce")


def parse_languages(languages: pd.Series) -> pd.Series:
    return languages.str.strip("|").str.split("|")


def load_and_clean_data(filepath: str) -> pd.DataFrame:

    df = pd.read_csv(filepath)

    if "gender" in df.columns:
        df["gender"] = clean_gender(df["gender"])

    if "posted_date" in df.columns:
        df["posted_date"] = parse_posted_date(df["posted_date"])

    if "languages" in df.columns:
        df["languages"] = parse_languages(df["languages"])

    return df
