from pathlib import Path
import json

from src.config.settings import (
    RAW_EMPLOYEE_PATH, RAW_DEPARTMENT_PATH, PROCESSED_EMPLOYEE_PATH,
    OUTPUT_DIR, CHART_DIR, REPORT_DIR, API_URL, API_TIMEOUT
)
from src.data.loader import DataLoader
from src.data.cleaner import DataCleaner
from src.analysis.analyzer import DataAnalyzer
from src.visualization.charts import VisualizationManager
from src.api.client import APIClient
from src.reports.generator import ReportGenerator
from src.utils.helpers import sanitize_names, high_salary_records, active_records, sort_records


def main() -> None:
    loader = DataLoader(RAW_EMPLOYEE_PATH, RAW_DEPARTMENT_PATH)
    raw = loader.load_employees()
    departments = loader.load_departments()
    profile = loader.inspect(raw)
    print('1. DATASET PROFILE')
    print('Shape:', profile['shape'])
    print('Head:\n', raw.head())
    print('Tail:\n', raw.tail())
    print('Describe:\n', raw.describe(include='all').transpose().head(15))
    print('Missing:', profile['missing_values'])
    print('Duplicates:', profile['duplicate_rows'])

    cleaner = DataCleaner(PROCESSED_EMPLOYEE_PATH)
    cleaned = cleaner.clean(raw)
    print('\n2. CLEANING COMPLETE')
    print('Cleaned shape:', cleaned.shape)

    analyzer = DataAnalyzer(cleaned, departments)
    numpy_metrics = analyzer.numpy_analysis()
    summary = analyzer.groupby_summary()
    merged = analyzer.merge_departments()
    findings = analyzer.findings(merged)

    print('\n3. NUMPY')
    print('Mean:', numpy_metrics['salary_mean'])
    print('Sum:', numpy_metrics['salary_sum'])
    print('Std:', numpy_metrics['salary_std'])
    print('First 10 salary values:', numpy_metrics['salary_first_10'])
    print('Broadcast example:', numpy_metrics['broadcast_first_3'])
    print('Dot product example:', numpy_metrics['dot_product_first_10'])

    print('\n4. PANDAS INDEXING / FILTERING')
    print('loc sample:\n', cleaned.loc[:2, ['employee_id', 'department', 'salary']])
    print('iloc sample:\n', cleaned.iloc[:3, :4])
    print('High salary count:', len(high_salary_records(cleaned, threshold=70000)))
    print('Active IT records:', len(active_records(cleaned, status='Active')))
    print('Sorted sample:\n', sort_records(cleaned, 'salary', 'performance_score').head())
    print('Sanitized names:', sanitize_names(cleaned['first_name'].head(5)))

    api_client = APIClient(API_URL, API_TIMEOUT, OUTPUT_DIR / 'api_cache.json')
    api_result = api_client.fetch()
    print('\n5. API RESULT')
    print(json.dumps(api_result, indent=2)[:1000])

    visualizer = VisualizationManager(CHART_DIR)
    charts = visualizer.create_all(cleaned, summary)
    print('\n6. CHARTS GENERATED')
    for chart in charts:
        print(chart)

    generator = ReportGenerator(REPORT_DIR, OUTPUT_DIR)
    generator.generate(raw, cleaned, summary, merged, numpy_metrics, api_result, charts, findings, profile['duplicate_rows'])
    print('\n7. FIVE BUSINESS FINDINGS')
    for finding in findings:
        print('-', finding)
    print('\nPipeline completed successfully.')


if __name__ == '__main__':
    main()
