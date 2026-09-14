import os
import pandas as pd
import matplotlib.pyplot as plt


def dashboard_agent(file_path, analysis_result=None, domain_config=None):
    """
    Production-style dynamic dashboard generator.

    The dashboard adapts to the structure of the incoming dataset by:
    - Detecting useful numeric measures
    - Detecting useful categorical dimensions
    - Detecting date columns
    - Prioritizing business-relevant fields
    - Creating appropriate visualizations
    - Generating a professional HTML dashboard
    """

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        charts = []

        # ---------------------------------------------------------
        # Detect numeric columns
        # ---------------------------------------------------------

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        # Remove ID-like numeric columns from business measures
        useful_numeric = [
            col for col in numeric_columns
            if not any(
                keyword in col.lower()
                for keyword in [
                    "id",
                    "postal",
                    "zip",
                    "code"
                ]
            )
        ]

        if not useful_numeric:
            useful_numeric = numeric_columns

        # ---------------------------------------------------------
        # Detect categorical columns
        # ---------------------------------------------------------

        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        # Remove ID-like and high-cardinality columns
        useful_categorical = []

        for col in categorical_columns:
            unique_count = df[col].nunique(dropna=True)

            if unique_count <= 20 and unique_count > 1:
                useful_categorical.append(col)

        # ---------------------------------------------------------
        # Detect date columns
        # ---------------------------------------------------------

        date_columns = []

        for col in df.columns:
            if "date" in col.lower():
                converted = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )

                if converted.notna().sum() > 0:
                    date_columns.append(col)

        # ---------------------------------------------------------
        # Prioritize important business measures
        # ---------------------------------------------------------

        priority_keywords = [
            "sales",
            "revenue",
            "profit",
            "amount",
            "income",
            "price",
            "cost",
            "quantity",
            "units",
            "salary",
            "fee",
            "balance",
            "stock",
            "inventory",
            "score"
        ]

        prioritized_numeric = []

        for keyword in priority_keywords:
            for col in useful_numeric:
                if keyword in col.lower() and col not in prioritized_numeric:
                    prioritized_numeric.append(col)

        for col in useful_numeric:
            if col not in prioritized_numeric:
                prioritized_numeric.append(col)

        useful_numeric = prioritized_numeric

        # ---------------------------------------------------------
        # Prioritize useful dimensions
        # ---------------------------------------------------------

        dimension_keywords = [
            "category",
            "segment",
            "region",
            "department",
            "product",
            "customer",
            "country",
            "city",
            "state",
            "type",
            "status",
            "plan",
            "supplier"
        ]

        prioritized_categories = []

        for keyword in dimension_keywords:
            for col in useful_categorical:
                if keyword in col.lower() and col not in prioritized_categories:
                    prioritized_categories.append(col)

        for col in useful_categorical:
            if col not in prioritized_categories:
                prioritized_categories.append(col)

        useful_categorical = prioritized_categories

        # ---------------------------------------------------------
        # Chart 1: Main metric distribution
        # ---------------------------------------------------------

        if useful_numeric:
            measure = useful_numeric[0]

            plt.figure(figsize=(10, 6))

            df[measure].dropna().plot(
                kind="hist",
                bins=20
            )

            plt.title(f"Distribution of {measure}")
            plt.xlabel(measure)
            plt.ylabel("Frequency")
            plt.tight_layout()

            chart_path = os.path.join(
                output_dir,
                "dashboard_metric_distribution.png"
            )

            plt.savefig(chart_path, dpi=150)
            plt.close()

            charts.append(chart_path)

        # ---------------------------------------------------------
        # Chart 2: Performance by business dimension
        # ---------------------------------------------------------

        if useful_categorical and useful_numeric:
            category = useful_categorical[0]
            measure = useful_numeric[0]

            grouped = (
                df.groupby(category)[measure]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            if not grouped.empty:
                plt.figure(figsize=(10, 6))

                grouped.sort_values().plot(
                    kind="barh"
                )

                plt.title(
                    f"Top {category} by {measure}"
                )

                plt.xlabel(measure)
                plt.ylabel(category)
                plt.tight_layout()

                chart_path = os.path.join(
                    output_dir,
                    "dashboard_dimension_performance.png"
                )

                plt.savefig(chart_path, dpi=150)
                plt.close()

                charts.append(chart_path)

        # ---------------------------------------------------------
        # Chart 3: Time trend when a date column exists
        # ---------------------------------------------------------

        if date_columns and useful_numeric:
            date_column = date_columns[0]
            measure = useful_numeric[0]

            temp = df.copy()

            temp[date_column] = pd.to_datetime(
                temp[date_column],
                errors="coerce"
            )

            temp[measure] = pd.to_numeric(
                temp[measure],
                errors="coerce"
            )

            temp = temp.dropna(
                subset=[date_column, measure]
            )

            if not temp.empty:
                trend = (
                    temp.groupby(date_column)[measure]
                    .sum()
                    .sort_index()
                )

                plt.figure(figsize=(10, 6))

                trend.plot()

                plt.title(
                    f"{measure} Over Time"
                )

                plt.xlabel("Date")
                plt.ylabel(measure)
                plt.tight_layout()

                chart_path = os.path.join(
                    output_dir,
                    "dashboard_time_trend.png"
                )

                plt.savefig(chart_path, dpi=150)
                plt.close()

                charts.append(chart_path)

        # ---------------------------------------------------------
        # Fallback relationship chart
        # ---------------------------------------------------------

        if len(charts) < 3 and len(useful_numeric) >= 2:
            x_column = useful_numeric[0]
            y_column = useful_numeric[1]

            plt.figure(figsize=(10, 6))

            plt.scatter(
                df[x_column],
                df[y_column],
                alpha=0.5
            )

            plt.title(
                f"{y_column} vs {x_column}"
            )

            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.tight_layout()

            chart_path = os.path.join(
                output_dir,
                "dashboard_numeric_relationship.png"
            )

            plt.savefig(chart_path, dpi=150)
            plt.close()

            charts.append(chart_path)

        # ---------------------------------------------------------
        # Determine domain title
        # ---------------------------------------------------------

        domain_title = "Dynamic Data Dashboard"

        if domain_config:
            domain_text = str(
                domain_config.get("domain", "")
            )

            if domain_text:
                domain_title = (
                    domain_text
                    .split("\n")[0]
                    .strip()
                )

        # ---------------------------------------------------------
        # Extract metrics
        # ---------------------------------------------------------

        metrics = {}

        if analysis_result:
            metrics = analysis_result.get(
                "metrics",
                {}
            )

        # ---------------------------------------------------------
        # Create HTML dashboard
        # ---------------------------------------------------------

        dashboard_path = os.path.join(
            output_dir,
            "dashboard.html"
        )

        html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Dynamic Data Dashboard</title>

<style>

body {{
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #1f2937;
}}

.container {{
    max-width: 1250px;
    margin: auto;
    padding: 35px;
}}

.header {{
    background: white;
    padding: 30px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}}

h1 {{
    margin: 0 0 8px 0;
    font-size: 32px;
}}

.subtitle {{
    color: #6b7280;
    font-size: 15px;
}}

.metrics {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(190px, 1fr));

    gap: 18px;
    margin-bottom: 25px;
}}

.metric {{
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
}}

.metric-name {{
    color: #6b7280;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.metric-value {{
    font-size: 25px;
    font-weight: bold;
    margin-top: 10px;
}}

.charts {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(480px, 1fr));

    gap: 22px;
}}

.chart {{
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
}}

.chart img {{
    width: 100%;
    height: auto;
    display: block;
}}

.footer {{
    margin-top: 25px;
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>{domain_title}</h1>

<div class="subtitle">
Production Dynamic Dashboard • Automatically generated from dataset structure
</div>

</div>

<div class="metrics">
"""

        for key, value in metrics.items():

            html += f"""
<div class="metric">

<div class="metric-name">
{key.replace("_", " ").title()}
</div>

<div class="metric-value">
{value}
</div>

</div>
"""

        html += """
</div>

<div class="charts">
"""

        for chart in charts:

            filename = os.path.basename(chart)

            html += f"""
<div class="chart">

<img
    src="{filename}"
    alt="{filename}"
>

</div>
"""

        html += """
</div>

<div class="footer">
Generated automatically by the Dynamic Dashboard Agent
</div>

</div>

</body>

</html>
"""

        with open(
            dashboard_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(html)

        print("\n[Dashboard Agent] Dashboard created successfully.")
        print(
            f"[Dashboard Agent] Useful numeric columns: "
            f"{useful_numeric}"
        )
        print(
            f"[Dashboard Agent] Useful dimensions: "
            f"{useful_categorical}"
        )
        print(
            f"[Dashboard Agent] Date columns: "
            f"{date_columns}"
        )
        print(
            f"[Dashboard Agent] Charts created: "
            f"{len(charts)}"
        )
        print(
            f"[Dashboard Agent] Dashboard: "
            f"{dashboard_path}"
        )

        return {
            "status": "success",
            "dashboard_path": dashboard_path,
            "charts": charts,
            "numeric_columns": useful_numeric,
            "categorical_columns": useful_categorical,
            "date_columns": date_columns
        }

    except FileNotFoundError as e:

        return {
            "status": "failed",
            "error": str(e)
        }

    except pd.errors.EmptyDataError:

        return {
            "status": "failed",
            "error": "The CSV file is empty or unreadable."
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": f"Dashboard generation failed: {str(e)}"
        }
