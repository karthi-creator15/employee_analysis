import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / '.env')

RAW_EMPLOYEE_PATH = PROJECT_ROOT / os.getenv('RAW_EMPLOYEE_PATH', 'data/raw/employees.csv')
RAW_DEPARTMENT_PATH = PROJECT_ROOT / os.getenv('RAW_DEPARTMENT_PATH', 'data/raw/departments.csv')
PROCESSED_EMPLOYEE_PATH = PROJECT_ROOT / os.getenv('PROCESSED_EMPLOYEE_PATH', 'data/processed/cleaned_employees.csv')
OUTPUT_DIR = PROJECT_ROOT / os.getenv('OUTPUT_DIR', 'outputs')
CHART_DIR = OUTPUT_DIR / 'charts'
REPORT_DIR = OUTPUT_DIR / 'reports'
API_URL = os.getenv('API_URL', 'https://api.frankfurter.app/latest?from=USD')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))

for directory in (RAW_EMPLOYEE_PATH.parent, RAW_DEPARTMENT_PATH.parent, PROCESSED_EMPLOYEE_PATH.parent, CHART_DIR, REPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
