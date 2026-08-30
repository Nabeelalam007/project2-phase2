import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Ensure the output folder exists to prevent FileNotFoundError
os.makedirs("output", exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY
)

class RetailState(TypedDict):
    raw_data: str
    cleaned_data: str
    analysis: str

def clean_agent(state: RetailState):
    df = pd.read_csv(state["raw_data"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Save cleaned dataset
    cleaned_path = "output/cleaned_superstore.csv"
    df.to_csv(cleaned_path, index=False)

    print("Clean Agent: Data cleaned successfully.")
    print(f"Rows after cleaning: {len(df)}")

    return {"cleaned_data": cleaned_path}

def analysis_agent(state: RetailState):
    df = pd.read_csv(state["cleaned_data"])
    total_sales = df["Sales"].sum()

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    sales_by_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    sales_by_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    response = llm.invoke(
        f"""
You are a retail data analyst.

Analyze these retail sales results and provide 3 concise business insights:

Total Sales: ${total_sales:,.2f}

Top 5 Products:
{top_products.to_string()}

Sales by Region:
{sales_by_region.to_string()}

Sales by Category:
{sales_by_category.to_string()}

Focus on the strongest-performing products, regions, and categories.
Do not invent information that is not present in the data.
"""
    )

    print("Gemini Business Insights:")
    print(response.content)
    analysis = f"""
Retail Sales Analysis

Total Sales: ${total_sales:,.2f}

Top 5 Products:
{top_products.to_string()}

Sales by Region:
{sales_by_region.to_string()}

Sales by Category:
{sales_by_category.to_string()}
"""

    with open("output/analysis.txt", "w", encoding="utf-8") as f:
        f.write(analysis)

    print("Analysis Agent: Analysis completed successfully.")

    return {"analysis": analysis}

def orchestrator(state: RetailState):
    print("Orchestrator: Starting pipeline...")
    print("Orchestrator: Routing to Clean Agent...")
    return state

def visualization_agent(state: RetailState):
    # Load dataset inside the agent
    df = pd.read_csv(state["cleaned_data"])

    # Sales by Region
    region_sales = df.groupby("Region")["Sales"].sum()
    region_sales.plot(kind="bar", title="Sales by Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("output/sales_by_region.png")
    plt.close()

    # Sales by Category
    category_sales = df.groupby("Category")["Sales"].sum()
    category_sales.plot(kind="bar", title="Sales by Category")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("output/sales_by_category.png")
    plt.close()

    # Top 5 Products
    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    top_products.plot(kind="barh", title="Top 5 Products by Sales")
    plt.xlabel("Total Sales")
    plt.tight_layout()
    plt.savefig("output/top_5_products.png")
    plt.close()

    print("Visualization Agent: Charts created successfully.")

    return state

graph = StateGraph(RetailState)

graph.add_node("orchestrator", orchestrator)
graph.add_node("clean_agent", clean_agent)
graph.add_node("analysis_agent", analysis_agent)
graph.add_node("visualization_agent", visualization_agent)

graph.add_edge(START, "orchestrator")
graph.add_edge("orchestrator", "clean_agent")
graph.add_edge("clean_agent", "analysis_agent")
graph.add_edge("analysis_agent", "visualization_agent")
graph.add_edge("visualization_agent", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({
        "raw_data": "data/samplesuperstore.csv",
        "cleaned_data": "",
        "analysis": ""
    })

    print("\nPipeline completed successfully!")
    print("\nAnalysis:")
    print(result["analysis"])