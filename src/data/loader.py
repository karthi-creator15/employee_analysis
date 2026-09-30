from pathlib import Path
from typing import Any
import pandas as pd
from src.utils.exceptions import InvalidDatasetError

REQUIRED_COLUMNS = {
    'employee_id', 'first_name', 'last_name', 'age', 'gender', 'department',
    'designation', 'salary', 'joining_date', 'experience', 'performance_score',
    'city', 'status', 'department_id'
}

class DataLoader:
    def __init__(self, employee_path: Path, department_path: Path) -> None:
        self.employee_path = employee_path
        self.department_path = department_path

    def load_employees(self) -> pd.DataFrame:
        if not self.employee_path.exists():
            raise FileNotFoundError(f'Employee file not found: {self.employee_path}')
        df = pd.read_csv(self.employee_path)
        self._validate(df)
        return df

    def load_departments(self) -> pd.DataFrame:
        if not self.department_path.exists():
            raise FileNotFoundError(f'Department file not found: {self.department_path}')
        return pd.read_csv(self.department_path)

    @staticmethod
    def _validate(df: pd.DataFrame) -> None:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise InvalidDatasetError(f'Missing mandatory columns: {sorted(missing)}')
        if df.empty:
            raise InvalidDatasetError('Dataset is empty.')
        if df['employee_id'].isna().all():
            raise InvalidDatasetError('employee_id cannot be entirely missing.')

    @staticmethod
    def inspect(df: pd.DataFrame) -> dict[str, Any]:
        return {
            'shape': list(df.shape),
            'columns': df.columns.tolist(),
            'dtypes': {k: str(v) for k, v in df.dtypes.items()},
            'missing_values': df.isna().sum().to_dict(),
            'duplicate_rows': int(df.duplicated().sum()),
        }
