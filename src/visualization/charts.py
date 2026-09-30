from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

class VisualizationManager:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _save(self, fig, filename: str) -> str:
        path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=160, bbox_inches='tight')
        plt.close(fig)
        return str(path)

    def bar_chart(self, summary: pd.DataFrame) -> str:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(summary['department'], summary['avg_salary'])
        ax.set_title('Average Salary by Department')
        ax.set_xlabel('Department')
        ax.set_ylabel('Average Salary')
        ax.grid(axis='y', alpha=0.3)
        ax.tick_params(axis='x', rotation=30)
        return self._save(fig, '01_average_salary_by_department.png')

    def line_chart(self, df: pd.DataFrame) -> str:
        trend = df.groupby(df['joining_date'].dt.to_period('M')).size().cumsum()
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(trend.index.astype(str), trend.values, marker='o', label='Cumulative joins')
        ax.set_title('Cumulative Employee Join Trend')
        ax.set_xlabel('Joining Month')
        ax.set_ylabel('Cumulative Employees')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        return self._save(fig, '02_cumulative_join_trend.png')

    def histogram(self, df: pd.DataFrame) -> str:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(df['salary'], bins=12, edgecolor='black')
        ax.set_title('Salary Distribution')
        ax.set_xlabel('Salary')
        ax.set_ylabel('Frequency')
        ax.grid(axis='y', alpha=0.3)
        return self._save(fig, '03_salary_distribution.png')

    def scatter(self, df: pd.DataFrame) -> str:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.scatter(df['experience'], df['salary'], alpha=0.65, label='Employees')
        ax.set_title('Years of Experience vs Salary')
        ax.set_xlabel('Years of Experience')
        ax.set_ylabel('Salary')
        ax.grid(True, alpha=0.3)
        ax.legend()
        return self._save(fig, '04_experience_vs_salary.png')

    def donut(self, df: pd.DataFrame) -> str:
        counts = df['department'].value_counts()
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.45})
        ax.set_title('Department Headcount Share')
        return self._save(fig, '05_department_headcount_share.png')

    def create_all(self, df: pd.DataFrame, summary: pd.DataFrame) -> list[str]:
        return [self.bar_chart(summary), self.line_chart(df), self.histogram(df), self.scatter(df), self.donut(df)]
