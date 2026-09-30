# Employee / Customer Data Analysis & Insights Platform

A modular Python OOP implementation of the GENAI / ML Engineer assessment. The pipeline follows:

**Ingest → Profile → Clean → Vectorize (NumPy) → Aggregate (Pandas) → Visualize → Enrich → Report**

## Tech Stack
Python 3.x, NumPy, Pandas, Matplotlib, Requests, python-dotenv, Git.

## Important dataset note
The assessment requires a realistic public dataset and forbids a trivial synthetic dataset. This project therefore includes `scripts/download_dataset.py`, which downloads the public `messy_HR_data.csv` dataset from the `eyowhite/Messy-dataset` GitHub repository and adapts it into the assessment schema. The source contains 1,000 employee rows and deliberately messy values. Review the source's license/terms before redistributing it.

## Setup

### Windows PowerShell / VS Code
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/download_dataset.py
python -m src.main
```

### Windows CMD
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts\download_dataset.py
python -m src.main
```

## OOP Design
- `DataLoader`: ingestion and schema validation
- `BaseDataProcessor`: abstract processing contract
- `EmployeeDataProcessor`: overridden `process()` implementation
- `DataCleaner`: cleaning orchestration
- `DataAnalyzer`: NumPy/Pandas computations and relational merge
- `VisualizationManager`: five Matplotlib charts
- `APIClient`: resilient REST API integration and JSON cache
- `ReportGenerator`: Markdown, JSON and text reports

## Git workflow
```bash
git init
git add .
git commit -m "chore: initialize employee analytics project"
git branch -M main

git checkout -b feature/data-cleaning
git add src/data
git commit -m "feat: add employee data cleaning pipeline"
git checkout main

git checkout -b feature/data-analysis
git add src/analysis
 git commit -m "feat: add numpy and pandas analysis"
git checkout main

git checkout -b feature/visualizations
git add src/visualization
git commit -m "feat: add five matplotlib visualizations"
git checkout main

git checkout -b feature/api-integration
git add src/api
 git commit -m "feat: add resilient REST API client"
git checkout main

git checkout -b feature/report-generation
git add src/reports
 git commit -m "feat: generate executive analysis reports"
git checkout main
```
