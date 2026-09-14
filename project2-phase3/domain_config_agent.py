import os
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def domain_config_agent(file_path):
    """
    Examines the incoming dataset and determines:
    - The likely domain
    - Important columns
    - Recommended business metrics
    - Useful analysis directions
    """

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        columns = list(df.columns)

        sample_data = df.head(5).to_string(index=False)

        llm = ChatGoogleGenerativeAI(
   model="gemini-3.6-flash"
)

        prompt = f"""
You are a Domain Configuration Agent in a production data analytics pipeline.

Analyze the incoming dataset and identify its business domain.

Dataset columns:
{columns}

Sample rows:
{sample_data}

Determine:
1. The most likely domain, such as retail sales, e-commerce,
   inventory, restaurant sales, subscriptions, finance, etc.
2. Which columns are important for analysis.
3. Which columns represent dimensions/categories.
4. Which columns represent numerical measures.
5. Three to five meaningful business success metrics.
6. Three useful analysis questions.

Return the result in a clear structured format.

Do not assume the dataset is a retail dataset.
Base your decisions only on the provided columns and sample data.
"""

        response = llm.invoke(prompt)

        return {
            "domain": response.content[0]["text"] if isinstance(response.content, list) else response.content,
            "columns": columns,
            "row_count": len(df)
        }

    except FileNotFoundError:
        return {
            "error": f"Dataset not found: {file_path}"
        }

    except pd.errors.EmptyDataError:
        return {
            "error": "The CSV file is empty or contains no readable data."
        }

    except Exception as e:
        return {
            "error": f"Domain configuration failed: {str(e)}"
        }