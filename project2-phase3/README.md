# Project 2 – Phase 3

## Production-Grade Dynamic Dashboard + Domain-Aware Agents

### DevSynt AI Automation Internship

---

## Overview

This project implements a production-oriented, domain-aware multi-agent data analytics pipeline.

Unlike a dashboard designed for only one fixed dataset, the system analyzes the structure of an incoming CSV dataset, identifies its business domain, determines important dimensions and measures, generates relevant KPIs, performs automated analysis, and dynamically creates dashboard visualizations.

The pipeline was tested across **five different business datasets** to verify that the agents can adapt to different dataset structures, column names, business domains, numerical measures, categorical dimensions, and date availability.

---

# Architecture

The pipeline consists of five major stages.

### 1. Domain Configuration Agent

* Identifies the business domain from the dataset schema and sample records.
* Classifies important columns into dimensions and numerical measures.
* Identifies relevant date fields.
* Suggests domain-specific KPIs.
* Generates domain-specific business questions.

### 2. Orchestrator Agent

* Coordinates the complete analytics pipeline.
* Receives the domain configuration.
* Loads and validates the incoming dataset.
* Routes the dataset through the required processing stages.

### 3. Clean Agent

* Loads the incoming CSV dataset.
* Removes duplicate records.
* Handles empty rows.
* Normalizes column names where required.
* Produces a cleaned dataset for downstream analysis.

### 4. Analysis Agent

* Calculates key business metrics.
* Performs domain-aware analysis.
* Uses the detected dataset structure.
* Generates a structured analysis report.

### 5. Dynamic Dashboard Agent

* Automatically detects useful numerical columns.
* Automatically detects categorical dimensions.
* Detects date columns when available.
* Selects suitable visualizations based on the dataset structure.
* Generates a standalone HTML dashboard.
* Generates supporting PNG charts.

---

# Architecture Flow

```text
Incoming CSV Dataset
        |
        v
Domain Configuration Agent
        |
        v
Orchestrator Agent
        |
        v
Clean Agent
        |
        v
Analysis Agent
        |
        v
Dynamic Dashboard Agent
        |
        v
HTML Dashboard + PNG Charts + Analysis Report
```

The architecture diagram is also available in:

```text
assets/flow-daigram(2).png
```

---

# Project Structure

```text
project2-phase3/
│
├── agents/
│   ├── __init__.py
│   ├── domain_config.py
│   ├── orchestrator.py
│   ├── clean.py
│   ├── analysis.py
│   └── dashboard.py
│
├── test-datasets/
│   ├── samplesuperstore.csv
│   ├── ecommerce_orders.csv
│   ├── inventory_stock.csv
│   ├── restaurant_sales.csv
│   └── saas_subscriptions.csv
│
├── assets/
│   ├── flow-daigram(2).png
│   └── prompt-evolution-log.png
│
├── output/
│   ├── cleaned_dataset.csv
│   ├── analysis_report.txt
│   ├── dashboard.html
│   ├── dashboard_metric_distribution.png
│   ├── dashboard_dimension_performance.png
│   └── dashboard_time_trend.png
│
├── main.py
├── .gitignore
└── README.md
```

---

# Technologies Used

* Python
* Pandas
* Matplotlib
* LangChain
* LangGraph
* Google Gemini
* python-dotenv
* HTML
* CSS
* JavaScript

---

# Multi-Domain Testing

The pipeline was tested using five datasets representing different business domains.

## 1. Retail / Superstore

**Dataset:** `samplesuperstore.csv`

**Domain identified:**

E-Commerce / Commercial Order Fulfillment & Merchandising

**Dataset characteristics:**

* 10,194 rows
* 21 columns
* Sales
* Profit
* Quantity
* Discount
* Category
* Region
* Customer information
* Order and shipping dates

**Result:** PASS

The system successfully identified retail sales metrics including:

* Total sales
* Total profit
* Profit margin
* Total quantity
* Unique orders
* Average order value

The Dynamic Dashboard Agent also detected useful numerical measures, categorical dimensions, and date fields.

---

## 2. E-Commerce Orders

**Dataset:** `ecommerce_orders.csv`

**Domain identified:**

E-Commerce / Multi-Category Retail Sales

**Dataset characteristics:**

* 20 rows
* 10 columns
* Orders
* Customers
* Products
* Categories
* Quantity
* Unit price
* Total sales
* Regions
* Payment methods

**Result:** PASS

The Domain Configuration Agent correctly identified the dataset as an e-commerce sales dataset.

The system generated domain-aware analysis around:

* Category performance
* Payment method usage
* Regional performance
* Sales trends
* Customer and order behavior

The Dynamic Dashboard Agent detected:

* `Total_Sales`
* `Unit_Price`
* `Quantity`

It also detected:

* `Order_Date`
* `Category`
* `Region`
* `Product`
* `Customer_ID`
* `Order_ID`
* `Payment_Method`

Three dashboard visualizations were generated successfully.

---

## 3. Inventory / Supply Chain

**Dataset:** `inventory_stock.csv`

**Domain identified:**

Inventory Management & Supply Chain Operations

**Dataset characteristics:**

* 15 rows
* 11 columns
* Stock levels
* Reorder levels
* Units received
* Units sold
* Unit cost
* Warehouses
* Suppliers
* Stock status

**Result:** PASS

The pipeline successfully processed the inventory dataset.

The system identified inventory-related business concepts and generated analysis based on the available schema.

The Dynamic Dashboard Agent detected useful numerical measures including:

* `Unit_Cost`
* `Units_Received`
* `Units_Sold`
* `Stock_Level`
* `Reorder_Level`

The inventory dataset also demonstrated that the pipeline can process datasets where the available structure differs from the original retail dataset.

Three dashboard charts were generated successfully.

---

## 4. Restaurant Sales

**Dataset:** `restaurant_sales.csv`

**Domain identified:**

Restaurant / Food Service Sales (POS Analytics)

**Dataset characteristics:**

* 15 rows
* 10 columns
* Menu items
* Food categories
* Quantity
* Unit price
* Revenue
* Dine-In / Takeaway
* Payment methods
* Staff
* Sale dates

**Result:** PASS

The Domain Configuration Agent correctly identified the dataset as restaurant / food service POS data.

The system generated domain-aware analysis around:

* Menu performance
* Category performance
* Dine-In vs. Takeaway
* Payment method usage
* Staff productivity
* Revenue contribution

The Dynamic Dashboard Agent detected:

* `Revenue`
* `Unit_Price`
* `Quantity`

and the date column:

* `Sale_Date`

Three dashboard charts were generated successfully.

---

## 5. SaaS / Subscription Analytics

**Dataset:** `saas_subscriptions.csv`

**Domain identified:**

SaaS / Subscription Business Analytics

**Dataset characteristics:**

* 15 rows
* 10 columns
* Subscription plans
* Monthly fees
* Users
* Active users
* Support tickets
* Churn status
* Regions
* Start dates

**Result:** PASS

The Domain Configuration Agent correctly identified the dataset as SaaS / subscription analytics.

The system generated SaaS-specific analysis around:

* Monthly recurring revenue
* Customer churn
* User and seat utilization
* Revenue per account
* Support activity
* Subscription plans

The Dynamic Dashboard Agent detected:

* `Monthly_Fee`
* `Users`
* `Active_Users`
* `Support_Tickets`

and the date column:

* `Start_Date`

Three dashboard charts were generated successfully.

---

# Testing Summary

| Dataset                  | Domain                   |   Rows | Columns | Domain Detection | Cleaning | Analysis | Dashboard |
| ------------------------ | ------------------------ | -----: | ------: | ---------------- | -------- | -------- | --------- |
| `samplesuperstore.csv`   | Retail                   | 10,194 |      21 | PASS             | PASS     | PASS     | PASS      |
| `ecommerce_orders.csv`   | E-Commerce               |     20 |      10 | PASS             | PASS     | PASS     | PASS      |
| `inventory_stock.csv`    | Inventory / Supply Chain |     15 |      11 | PASS             | PASS     | PASS     | PASS      |
| `restaurant_sales.csv`   | Restaurant / F&B         |     15 |      10 | PASS             | PASS     | PASS     | PASS      |
| `saas_subscriptions.csv` | SaaS / Subscriptions     |     15 |      10 | PASS             | PASS     | PASS     | PASS      |

## Overall Testing Result

**5/5 datasets successfully processed.**

The tests demonstrate that the pipeline can adapt to:

* Different column names
* Different numerical measures
* Different categorical dimensions
* Different business domains
* Datasets with dates
* Different dataset sizes
* Different business KPIs
* Different analytical requirements

---

# Dynamic Dashboard Behavior

The dashboard is not tied to one specific dataset.

Instead, the Dynamic Dashboard Agent inspects the incoming dataset and dynamically determines which fields are useful for visualization.

## Numerical Columns

The agent searches for useful numeric fields and prioritizes business measures such as:

* Sales
* Revenue
* Profit
* Quantity
* Cost
* Price
* Fees
* Inventory measures

Identifier-like numeric columns are filtered where possible.

## Dimensions

The agent detects useful categorical fields.

Examples include:

* Category
* Region
* Segment
* Product
* Warehouse
* Payment Method
* Plan
* Staff
* Table Type

## Date Columns

The dashboard searches for date-like columns and converts them when possible.

If a suitable date column is available, a time-trend visualization can be generated.

If no suitable date column exists, the dashboard continues without requiring a time-trend chart.

## Visualization Strategy

Depending on the available dataset structure, the dashboard can generate visualizations such as:

* Numeric metric distributions
* Dimension performance
* Time trends
* Numeric relationships as a fallback

This allows the dashboard to remain useful across different datasets instead of depending on fixed column names.

---

# Error Handling

The pipeline includes handling for unexpected data conditions.

Examples include:

* Missing files
* Empty datasets
* Invalid CSV structures
* Missing expected columns
* Missing date columns
* Insufficient numerical columns
* Insufficient categorical dimensions

Instead of assuming that every dataset has the same structure, the agents inspect the available schema before performing analysis.

---

# Prompt Evolution / Versioning

The prompts were progressively refined during multi-domain testing.

## Version 1 – Initial Domain Prompt

**Focus:** Identify the dataset's business domain and important columns.

**Observation:**

The initial prompt could identify the general domain, but the generated analysis could become too focused on common retail concepts when the dataset structure changed.

**Improvement:**

The prompt was expanded to explicitly request:

* Business domain
* Important columns
* Dimensions
* Numerical measures
* Domain-specific KPIs
* Business questions

---

## Version 2 – Domain-Aware Analysis

**Focus:** Make recommendations depend on the detected business domain.

**Observation:**

Different domains contain different business concepts.

For example:

* Inventory requires stock and reorder metrics.
* Restaurants require menu and service-channel metrics.
* SaaS requires churn and recurring-revenue metrics.

**Improvement:**

The prompt was refined to instruct the model to derive KPIs and business questions from the detected schema instead of assuming retail sales metrics.

---

## Version 3 – Production / Adaptive Prompt

**Focus:** Improve consistency across different datasets.

The prompt emphasizes:

* Schema-first reasoning
* Explicit column classification
* Domain-specific KPIs
* Domain-specific business questions
* Avoiding unsupported assumptions
* Using only columns available in the dataset

**Result:**

The final configuration successfully processed all five test domains.

---

# Prompt Evolution Log

| Version | Change                                                 | Reason                                          |
| ------- | ------------------------------------------------------ | ----------------------------------------------- |
| v1.0    | Basic domain identification                            | Establish initial domain detection              |
| v1.1    | Added column classification                            | Improve dimension/measure detection             |
| v1.2    | Added domain-specific KPIs                             | Avoid generic analysis across domains           |
| v1.3    | Added business questions                               | Produce more useful analytical output           |
| v1.4    | Added schema-first and unsupported-assumption guidance | Improve reliability across different structures |
| v1.5    | Production-oriented adaptive configuration             | Improve consistency across multiple domains     |

The visual prompt evolution record is available at:

```text
assets/prompt-evolution-log.png
```

---

# Production-Grade Features

The project implements the following production-oriented features:

* Domain-aware configuration
* Dynamic dashboard generation
* Multi-agent orchestration
* Dataset cleaning
* Automated analysis
* Domain-aware KPIs
* Dynamic schema detection
* Date-column detection
* Error handling
* Consistent output structure
* Multiple-domain testing
* Prompt versioning
* Prompt evolution documentation
* Reusable agent modules
* Automatically generated charts
* Automatically generated analysis reports
* Standalone HTML dashboard

---

# Output Files

After a successful run, the pipeline generates:

```text
output/

├── cleaned_dataset.csv
├── analysis_report.txt
├── dashboard.html
├── dashboard_metric_distribution.png
├── dashboard_dimension_performance.png
└── dashboard_time_trend.png
```

Depending on the dataset structure, an additional numeric relationship chart may also be generated.

---

# How to Run

## 1. Activate the virtual environment

On Windows CMD:

```text
.venv\Scripts\activate
```

## 2. Configure the Gemini API key

Create or update the `.env` file:

```text
GOOGLE_API_KEY=your_api_key_here
```

## 3. Select a dataset

In `main.py`, set the dataset path:

```python
DATASET_PATH = "test-datasets/samplesuperstore.csv"
```

For example:

```python
DATASET_PATH = "test-datasets/ecommerce_orders.csv"
```

or:

```python
DATASET_PATH = "test-datasets/inventory_stock.csv"
```

or:

```python
DATASET_PATH = "test-datasets/restaurant_sales.csv"
```

or:

```python
DATASET_PATH = "test-datasets/saas_subscriptions.csv"
```

## 4. Run the pipeline

```text
python main.py
```

## 5. Open the generated dashboard

After a successful run:

```text
output/dashboard.html
```

Open the HTML file in a web browser to view the dynamically generated dashboard.

---

# Conclusion

Project 2 Phase 3 upgrades the previous multi-agent analytics pipeline into a more production-oriented and adaptive system.

The addition of the **Domain Configuration Agent** allows the system to understand what type of business data it is receiving before analysis begins.

The **Dynamic Dashboard Agent** removes dependence on a single fixed dataset structure by automatically detecting useful measures, dimensions, and date fields.

The pipeline was successfully validated using five different datasets representing:

1. Retail
2. E-Commerce
3. Inventory / Supply Chain
4. Restaurant / Food & Beverage
5. SaaS / Subscription Analytics

The successful tests demonstrate that the system can adapt its domain configuration, cleaning, analysis, and dashboard generation to different dataset structures.

## Final Validation

**5/5 datasets successfully processed.**

**Project 2 – Phase 3 successfully completed.**
