import pandas as pd

from data_clean import clean_gender, parse_languages, parse_posted_date


def test_clean_gender():
    genders = pd.Series([" f ", "M", " f", "m ", None])
    result = clean_gender(genders)
    expected = pd.Series(["F", "M", "F", "M", None])

    assert result.equals(expected)


def test_parse_posted_date():
    dates = pd.Series(["2011-10-24T17:50:06Z", "invalid_date_string", None])
    result = parse_posted_date(dates)
    expected = pd.Series([pd.Timestamp("2011-10-24 17:50:06+00:00"), pd.NaT, pd.NaT])

    assert result.equals(expected)


def test_parse_languages():
    languages = pd.Series(
        [
            "es|en|",
            "en",
            "fr|ar|es",
            None,
        ]
    )
    result = parse_languages(languages)

    expected = pd.Series([["es", "en"], ["en"], ["fr", "ar", "es"], None])

    assert result.equals(expected)
