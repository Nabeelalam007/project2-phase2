import os
import pandas as pd


def clean_agent(file_path):
    """
    Cleans an incoming CSV dataset for downstream analysis.

    Handles:
    - Missing files
    - Empty files
    - Duplicate rows
    - Empty rows
    - Whitespace in column names
    - Missing values
    - Numeric conversion where appropriate
    """

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        original_rows = len(df)

        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Replace empty strings with missing values
        df = df.replace(r"^\s*$", pd.NA, regex=True)

        # Remove columns that contain no useful data
        df = df.dropna(axis=1, how="all")

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "cleaned_dataset.csv")

        df.to_csv(output_path, index=False)

        print("\n[Clean Agent] Cleaning completed successfully.")
        print(f"[Clean Agent] Original rows: {original_rows}")
        print(f"[Clean Agent] Cleaned rows: {len(df)}")
        print(f"[Clean Agent] Columns: {len(df.columns)}")
        print(f"[Clean Agent] Output: {output_path}")

        return {
            "status": "success",
            "input_path": file_path,
            "output_path": output_path,
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "columns": list(df.columns)
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
            "error": f"Cleaning failed: {str(e)}"
        }
