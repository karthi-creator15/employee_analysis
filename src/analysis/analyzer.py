from typing import Any
import numpy as np
import pandas as pd

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame, departments: pd.DataFrame) -> None:
        self.df = df.copy()
        self.departments = departments.copy()

    def numpy_analysis(self) -> dict[str, Any]:
        salaries = self.df['salary'].to_numpy(dtype=float)
        sample_1d = salaries[:10]
        sample_2d = salaries[:10].reshape(-1, 1)
        inflation_adjusted = sample_2d * 1.05  # broadcasting
        performance_matrix = self.df[['performance_score', 'experience']].to_numpy(dtype=float)
        exp_max = max(float(self.df['experience'].max()), 1.0)
        performance_matrix[:, 1] = performance_matrix[:, 1] / exp_max
        weight_vector = np.array([0.70, 0.30])
        composite_score = np.dot(performance_matrix, weight_vector)
        return {
            'salary_mean': float(np.mean(salaries)),
            'salary_sum': float(np.sum(salaries)),
            'salary_std': float(np.std(salaries)),
            'salary_first_10': sample_1d.tolist(),
            'broadcast_first_3': inflation_adjusted[:3, 0].round(2).tolist(),
            'dot_product_first_10': composite_score[:10].round(4).tolist(),
        }

    def groupby_summary(self) -> pd.DataFrame:
        return self.df.groupby('department', as_index=False).agg(
            employee_count=('employee_id', 'count'),
            avg_salary=('salary', 'mean'),
            max_salary=('salary', 'max'),
            avg_performance=('performance_score', 'mean'),
        ).sort_values('avg_salary', ascending=False)

    def merge_departments(self) -> pd.DataFrame:
        department_info = self.departments[['department_id', 'budget']].copy()

        merged = pd.merge(
        self.df,
        department_info,
        on='department_id',
        how='left',
        validate='many_to_one'
    )

        merged['payroll'] = merged.groupby('department_id')['salary'].transform('sum')

        merged['budget_utilization_pct'] = np.where(
        merged['budget'].gt(0),
        merged['payroll'] / merged['budget'] * 100,
        np.nan
    )
        return merged

    def findings(self, merged: pd.DataFrame) -> list[str]:
        summary = self.groupby_summary()
        highest = summary.iloc[0]
        lowest = summary.iloc[-1]
        corr = float(self.df['experience'].corr(self.df['salary'])) if self.df['experience'].nunique() > 1 else 0.0
        max_budget = merged.groupby('department', as_index=False)['budget_utilization_pct'].mean().sort_values('budget_utilization_pct', ascending=False).iloc[0]
        performance = summary.sort_values('avg_performance', ascending=False).iloc[0]
        return [
            f"{highest['department']} has the highest average salary at {highest['avg_salary']:,.2f}.",
            f"{lowest['department']} has the lowest average salary at {lowest['avg_salary']:,.2f}.",
            f"The Pearson correlation between experience and salary is {corr:.3f}.",
            f"{max_budget['department']} has the highest mean payroll-to-budget utilization at {max_budget['budget_utilization_pct']:.2f}%.",
            f"{performance['department']} has the highest average performance score at {performance['avg_performance']:.2f}.",
        ]
