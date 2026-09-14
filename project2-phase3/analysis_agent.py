import os
import pandas as pd


def analysis_agent(file_path, domain_config):
    """
    Performs domain-aware analysis using the cleaned dataset.

    The agent dynamically selects metrics based on the available
    columns and the domain identified by the Domain Configuration Agent.
    """

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        results = {
            "status": "success",
            "domain": domain_config.get("domain", "Unknown"),
            "row_count": len(df),
            "column_count": len(df.columns),
            "metrics": {}
        }

        # Convert numeric columns safely
        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        def numeric_sum(column):
            if column in df.columns:
                return pd.to_numeric(
                    df[column], errors="coerce"
                ).sum()
            return None

        # ---------------------------------------------------------
        # Common business metrics
        # ---------------------------------------------------------

        revenue_columns = [
            "Sales",
            "Revenue",
            "Total_Sales",
            "Amount",
            "Total_Revenue"
        ]

        revenue_column = next(
            (col for col in revenue_columns if col in df.columns),
            None
        )

        if revenue_column:
            total_revenue = numeric_sum(revenue_column)

            if total_revenue is not None:
                results["metrics"]["total_revenue"] = round(
                    float(total_revenue), 2
                )

        # Profit
        if "Profit" in df.columns:
            profit = numeric_sum("Profit")

            if profit is not None:
                results["metrics"]["total_profit"] = round(
                    float(profit), 2
                )

                if revenue_column:
                    revenue = numeric_sum(revenue_column)

                    if revenue and revenue != 0:
                        results["metrics"]["profit_margin_percent"] = round(
                            float((profit / revenue) * 100), 2
                        )

        # Quantity
        quantity_columns = [
            "Quantity",
            "Units_Sold",
            "Units Sold"
        ]

        quantity_column = next(
            (col for col in quantity_columns if col in df.columns),
            None
        )

        if quantity_column:
            quantity = numeric_sum(quantity_column)

            if quantity is not None:
                results["metrics"]["total_quantity"] = int(quantity)

        # ---------------------------------------------------------
        # E-commerce / retail metrics
        # ---------------------------------------------------------

        order_id_column = next(
            (
                col for col in ["Order ID", "Order_ID", "OrderID"]
                if col in df.columns
            ),
            None
        )

        if order_id_column and revenue_column:
            unique_orders = df[order_id_column].nunique()

            if unique_orders > 0:
                revenue = numeric_sum(revenue_column)

                results["metrics"]["unique_orders"] = int(unique_orders)

                if revenue is not None:
                    results["metrics"]["average_order_value"] = round(
                        float(revenue / unique_orders), 2
                    )

        # ---------------------------------------------------------
        # Inventory metrics
        # ---------------------------------------------------------

        if "Stock_Level" in df.columns:
            stock = numeric_sum("Stock_Level")

            if stock is not None:
                results["metrics"]["total_stock_level"] = int(stock)

        if "Units_Received" in df.columns:
            received = numeric_sum("Units_Received")

            if received is not None:
                results["metrics"]["total_units_received"] = int(received)

        if "Units_Sold" in df.columns:
            sold = numeric_sum("Units_Sold")

            if sold is not None:
                results["metrics"]["total_units_sold"] = int(sold)

        if "Reorder_Level" in df.columns:
            reorder = numeric_sum("Reorder_Level")

            if reorder is not None:
                results["metrics"]["total_reorder_level"] = int(reorder)

        if "Stock_Level" in df.columns and "Reorder_Level" in df.columns:
            reorder_items = (
                df["Stock_Level"] < df["Reorder_Level"]
            ).sum()

            results["metrics"]["items_below_reorder_level"] = int(
                reorder_items
            )

        # ---------------------------------------------------------
        # SaaS / subscription metrics
        # ---------------------------------------------------------

        if "Monthly_Fee" in df.columns:
            monthly_fee = numeric_sum("Monthly_Fee")

            if monthly_fee is not None:
                results["metrics"]["total_monthly_recurring_revenue"] = round(
                    float(monthly_fee), 2
                )

        if "Active_Users" in df.columns and "Users" in df.columns:
            total_users = numeric_sum("Users")
            active_users = numeric_sum("Active_Users")

            if total_users and total_users != 0:
                results["metrics"]["active_user_rate_percent"] = round(
                    float((active_users / total_users) * 100), 2
                )

        if "Churned" in df.columns:
            churned_count = (
                df["Churned"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("yes")
                .sum()
            )

            results["metrics"]["churned_subscriptions"] = int(
                churned_count
            )

            results["metrics"]["churn_rate_percent"] = round(
                float((churned_count / len(df)) * 100), 2
            )

        # ---------------------------------------------------------
        # Category performance
        # ---------------------------------------------------------

        category_column = next(
            (
                col for col in [
                    "Category",
                    "Plan",
                    "Product_Category"
                ]
                if col in df.columns
            ),
            None
        )

        if category_column and revenue_column:
            category_performance = (
                df.groupby(category_column)[revenue_column]
                .sum()
                .sort_values(ascending=False)
                .round(2)
                .to_dict()
            )

            results["category_performance"] = category_performance

        # ---------------------------------------------------------
        # Regional performance
        # ---------------------------------------------------------

        if "Region" in df.columns and revenue_column:
            region_performance = (
                df.groupby("Region")[revenue_column]
                .sum()
                .sort_values(ascending=False)
                .round(2)
                .to_dict()
            )

            results["region_performance"] = region_performance

        # ---------------------------------------------------------
        # Domain information
        # ---------------------------------------------------------

        results["analysis_summary"] = {
            "domain": domain_config.get("domain", "Unknown"),
            "numeric_columns": numeric_columns,
            "available_columns": list(df.columns)
        }

        # ---------------------------------------------------------
        # Save analysis report
        # ---------------------------------------------------------

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        report_path = os.path.join(
            output_dir,
            "analysis_report.txt"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("DOMAIN-AWARE ANALYSIS REPORT\n")
            file.write("=" * 50 + "\n\n")

            file.write(
                f"Domain: {domain_config.get('domain', 'Unknown')}\n"
            )

            file.write(f"Rows analyzed: {len(df)}\n")
            file.write(f"Columns analyzed: {len(df.columns)}\n\n")

            file.write("KEY METRICS\n")
            file.write("-" * 50 + "\n")

            for key, value in results["metrics"].items():
                file.write(f"{key}: {value}\n")

            if "category_performance" in results:
                file.write("\nCATEGORY / PLAN PERFORMANCE\n")
                file.write("-" * 50 + "\n")

                for category, value in results[
                    "category_performance"
                ].items():
                    file.write(f"{category}: {value}\n")

            if "region_performance" in results:
                file.write("\nREGIONAL PERFORMANCE\n")
                file.write("-" * 50 + "\n")

                for region, value in results[
                    "region_performance"
                ].items():
                    file.write(f"{region}: {value}\n")

        results["report_path"] = report_path

        print("\n[Analysis Agent] Analysis completed successfully.")
        print(f"[Analysis Agent] Domain: {results['domain']}")
        print(f"[Analysis Agent] Rows analyzed: {len(df)}")
        print(
            f"[Analysis Agent] Metrics generated: "
            f"{len(results['metrics'])}"
        )
        print(f"[Analysis Agent] Report: {report_path}")

        return results

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
            "error": f"Analysis failed: {str(e)}"
        }