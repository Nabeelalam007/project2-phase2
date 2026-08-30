Retail Sales Analytics Dashboard

Project 2 - Phase 2 | Multi-Agent Retail Data Pipeline

Overview

This project implements a multi-agent retail data pipeline using Python, LangGraph, LangChain, and Google Gemini.

Agents

- Orchestrator Agent - Coordinates the complete pipeline.
- Clean Agent - Cleans the retail sales CSV data.
- Analysis Agent - Calculates sales insights and business metrics.
- Visualization Agent - Creates charts for the dashboard.

Dataset

The project uses the Superstore retail sales dataset:

data/samplesuperstore.csv

After cleaning, the dataset contains 10,194 rows.

Analysis Results

Total Sales: $2,326,534.35

Top Category: Technology - $839,893.28

Highest-Sales Region: West - $739,813.61

Top 5 Products

1. Canon imageCLASS 2200 Advanced Copier - $61,599.82
2. Fellowes PB500 Electric Punch Plastic Comb Binding Machine - $27,453.38
3. Cisco TelePresence System EX90 Videoconferencing Unit - $22,638.48
4. HON 5400 Series Task Chairs for Big and Tall - $21,870.58
5. GBC DocuBind TL300 Electric Binding System - $19,823.48

Dashboard

The project includes a dashboard located at:

docs/index.html

The dashboard presents:

- Total sales
- Cleaned row count
- Sales by region
- Sales by category
- Top 5 products
- AI-generated business insights

Visualizations

Generated charts are stored in the output folder:

- sales_by_region.png
- sales_by_category.png
- top_5_products.png

Technologies

- Python
- Pandas
- Matplotlib
- LangChain
- LangGraph
- Google Gemini
- HTML
- CSS

Project Structure

project2-phase2/
- data/samplesuperstore.csv
- docs/index.html
- output/analysis.txt
- output/cleaned_superstore.csv
- output/sales_by_category.png
- output/sales_by_region.png
- output/top_5_products.png
- .gitignore
- README.md
- requirements.txt
- retail_agents.py

Note: The .env file containing the Gemini API key and the .venv virtual environment are intentionally excluded from the GitHub submission.