"""Download a public messy HR CSV and adapt it to the assessment schema.

Source: https://github.com/eyowhite/Messy-dataset/blob/main/messy_HR_data.csv
The source is intentionally messy and contains 1,000 data rows, making it useful
for demonstrating missing-value handling, type coercion and cleaning.
"""
from pathlib import Path
from io import StringIO
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
URL = 'https://raw.githubusercontent.com/eyowhite/Messy-dataset/main/messy_HR_data.csv'


def main() -> None:
    raw_bytes = urllib.request.urlopen(URL, timeout=20).read()
    source = pd.read_csv(StringIO(raw_bytes.decode('utf-8')))
    source.to_csv(RAW / 'source_messy_hr.csv', index=False)

    # Adapt the public source to the assessment's employee schema.
    df = source.copy()
    df.insert(0, 'employee_id', range(100001, 100001 + len(df)))
    names = df['Name'].fillna('Unknown Unknown').astype(str).str.strip().str.split()
    df['first_name'] = names.str[0].fillna('Unknown')
    df['last_name'] = names.str[-1].fillna('Unknown')
    df['experience'] = pd.to_numeric(df['Age'], errors='coerce').sub(22).clip(lower=0)
    df['performance_score'] = df['Performance Score'].map({'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1})
    df['city'] = df['Department'].map({
        'IT': 'Chennai', 'Finance': 'Bengaluru', 'HR': 'Hyderabad',
        'Sales': 'Mumbai', 'Marketing': 'Pune'
    }).fillna('Chennai')
    df['status'] = df['Performance Score'].map(lambda x: 'Active' if str(x).upper() != 'F' else 'Review')
    dept_map = {'IT': 1, 'Finance': 2, 'HR': 3, 'Sales': 4, 'Marketing': 5}
    df['department_id'] = df['Department'].map(dept_map).fillna(99).astype(int)
    df = df.rename(columns={
        'Gender': 'gender', 'Department': 'department', 'Position': 'designation',
        'Salary': 'salary', 'Joining Date': 'joining_date'
    })
    df = df[['employee_id', 'first_name', 'last_name', 'Age', 'gender', 'department',
             'designation', 'salary', 'joining_date', 'experience', 'performance_score',
             'city', 'status', 'department_id']].rename(columns={'Age': 'age'})
    df.to_csv(RAW / 'employees.csv', index=False)

    departments = pd.DataFrame([
        [1, 'IT', 18000000, 'Head of Technology', 250],
        [2, 'Finance', 12000000, 'Finance Director', 120],
        [3, 'HR', 9000000, 'HR Director', 100],
        [4, 'Sales', 15000000, 'Sales Director', 180],
        [5, 'Marketing', 10000000, 'Marketing Director', 120],
    ], columns=['department_id', 'department', 'budget', 'division_head', 'target_headcount'])
    departments.to_csv(RAW / 'departments.csv', index=False)
    print(f'Created {RAW / "employees.csv"} with {len(df)} records.')

if __name__ == '__main__':
    main()
