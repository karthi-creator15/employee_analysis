from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np
import pandas as pd

class BaseDataProcessor(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    @abstractmethod
    def process(self) -> pd.DataFrame:
        raise NotImplementedError

class EmployeeDataProcessor(BaseDataProcessor):
    def __init__(self, df: pd.DataFrame, output_path: Path) -> None:
        super().__init__(df)
        self.output_path = output_path

    def process(self) -> pd.DataFrame:
        df = self.df
        text_columns = ['first_name', 'last_name', 'gender', 'department', 'designation', 'city', 'status']
        for column in text_columns:
            df[column] = df[column].astype('string').str.strip()
            df[column] = df[column].replace({'': pd.NA, 'nan': pd.NA, 'NAN': pd.NA, 'None': pd.NA})

        for column in ['age', 'salary', 'experience', 'performance_score']:
            df[column] = pd.to_numeric(df[column], errors='coerce')

        df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')
        df['employee_id'] = pd.to_numeric(df['employee_id'], errors='coerce').astype('Int64')

        df = df.drop_duplicates().copy()

        for column in ['age', 'salary', 'experience', 'performance_score']:
            median = df[column].median()
            df[column] = df[column].fillna(median)

        for column in ['gender', 'department', 'designation', 'city', 'status', 'joining_date']:
            mode = df[column].mode(dropna=True)
            if not mode.empty:
                df[column] = df[column].fillna(mode.iloc[0])

        df['age'] = df['age'].clip(18, 80).round().astype(int)
        df['salary'] = df['salary'].clip(lower=0).round(2)
        df['experience'] = df['experience'].clip(lower=0).round(1)
        df['performance_score'] = df['performance_score'].clip(0, 5).round(2)
        df['joining_date'] = pd.to_datetime(df['joining_date'])
        df = df.sort_values('employee_id').reset_index(drop=True)
        df.to_csv(self.output_path, index=False)
        return df

class DataCleaner:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        return EmployeeDataProcessor(df, self.output_path).process()
