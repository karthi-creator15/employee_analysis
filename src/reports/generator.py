import json
from pathlib import Path
from typing import Any
import pandas as pd

class ReportGenerator:
    def __init__(self, report_dir: Path, output_dir: Path) -> None:
        self.report_dir = report_dir
        self.output_dir = output_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, raw: pd.DataFrame, cleaned: pd.DataFrame, summary: pd.DataFrame,
                 merged: pd.DataFrame, numpy_metrics: dict[str, Any], api_result: dict[str, Any],
                 charts: list[str], findings: list[str], duplicate_count: int) -> dict[str, Any]:
        metrics = {
            'raw_records': int(len(raw)),
            'cleaned_records': int(len(cleaned)),
            'duplicates_removed': int(duplicate_count),
            'missing_values_after_cleaning': int(cleaned.isna().sum().sum()),
            'average_salary': float(cleaned['salary'].mean()),
            'median_salary': float(cleaned['salary'].median()),
            'average_experience': float(cleaned['experience'].mean()),
            'average_performance': float(cleaned['performance_score'].mean()),
            'department_count': int(cleaned['department'].nunique()),
            'api_status_code': api_result.get('status_code'),
            'api_error': api_result.get('error'),
            'numpy': numpy_metrics,
            'department_summary': summary.round(2).to_dict(orient='records'),
            'findings': findings,
            'charts': charts,
        }
        (self.output_dir / 'analysis_summary.json').write_text(json.dumps(metrics, indent=4, default=str), encoding='utf-8')
        txt = '\n'.join([
            'EXECUTIVE ANALYSIS SUMMARY',
            '=' * 28,
            f"Records: {metrics['cleaned_records']}",
            f"Average salary: {metrics['average_salary']:,.2f}",
            f"Average experience: {metrics['average_experience']:.2f} years",
            f"Average performance: {metrics['average_performance']:.2f}",
            '', 'KEY FINDINGS:', *[f'- {item}' for item in findings],
        ])
        (self.output_dir / 'analysis_summary.txt').write_text(txt, encoding='utf-8')

        chart_lines = '\n'.join(f'![Chart {i}]({Path(path).as_posix()})' for i, path in enumerate(charts, 1))
        report = f"""# Employee Data Analysis & Insights Report

## Executive Summary
This report presents an end-to-end analysis of the employee dataset after validation, cleaning, numerical analysis, relational enrichment and visualization.

## Dataset Overview
- Raw records: {len(raw)}
- Cleaned records: {len(cleaned)}
- Departments: {cleaned['department'].nunique()}
- Duplicate rows removed: {duplicate_count}

## Data Quality Audit
- Missing values after cleaning: {int(cleaned.isna().sum().sum())}
- Numeric columns were coerced with `pd.to_numeric(..., errors='coerce')`.
- Dates were standardized with `pd.to_datetime(..., errors='coerce')`.
- Numeric missing values were median-imputed; categorical missing values used the mode.

## Statistical Findings

{summary.round(2).to_markdown(index=False)}

## NumPy Analysis
- Mean salary: {numpy_metrics['salary_mean']:,.2f}
- Salary standard deviation: {numpy_metrics['salary_std']:,.2f}
- Dot product composite scores were calculated from performance and normalized experience weights.
- Broadcasting was demonstrated by applying a 5% factor to a salary matrix.

## External API Enrichment
- Endpoint: `{api_result.get('source_url')}`
- HTTP status: `{api_result.get('status_code')}`
- Error: `{api_result.get('error')}`

## Visualizations
{chart_lines}

## Key Findings
{chr(10).join(f'- {finding}' for finding in findings)}

## Actionable Recommendations
- Review compensation bands by department using the observed salary distribution.
- Investigate departments with high payroll-to-budget utilization.
- Use experience and performance together when reviewing compensation patterns.
- Improve upstream data validation for missing and inconsistent fields.
- Re-run the pipeline periodically so findings remain tied to the latest available records.
"""
        (self.report_dir / 'analysis_report.md').write_text(report, encoding='utf-8')
        return metrics
