from typing import Any, Iterable
import pandas as pd

def sanitize_names(values: Iterable[Any]) -> list[str]:
    return list(map(lambda value: str(value).strip().title(), values))

def high_salary_records(df: pd.DataFrame, threshold: float = 70000) -> pd.DataFrame:
    return df[df['salary'] > threshold].copy()

def active_records(df: pd.DataFrame, **filters: Any) -> pd.DataFrame:
    result = df.copy()
    for column, value in filters.items():
        if column in result.columns:
            result = result[result[column] == value]
    return result

def sort_records(df: pd.DataFrame, *columns: str) -> pd.DataFrame:
    return df.sort_values(list(columns), ascending=False)
