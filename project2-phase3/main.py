import os

from agents.domain_config_agent import domain_config_agent
from agents.orchestrator_agent import orchestrator_agent
from agents.clean_agent import clean_agent
from agents.analysis_agent import analysis_agent
from agents.dashboard_agent import dashboard_agent
DATASET_PATH = "test-datasets/saas_subscriptions.csv"


def run_pipeline(file_path):
    print("\n========================================")
    print("PROJECT 2 PHASE 3")
    print("PRODUCTION DATA ANALYTICS PIPELINE")
    print("========================================")

    # ---------------------------------------------------------
    # 1. Domain Configuration Agent
    # ---------------------------------------------------------

    print("\n[1/4] Domain Configuration Agent")

    domain_config = domain_config_agent(file_path)

    if domain_config.get("error"):
        print(f"[ERROR] {domain_config['error']}")
        return

    print("[OK] Domain configuration completed.")

    # ---------------------------------------------------------
    # 2. Orchestrator Agent
    # ---------------------------------------------------------

    print("\n[2/4] Orchestrator Agent")

    orchestration = orchestrator_agent(
        file_path,
        domain_config
    )

    if orchestration.get("status") != "ready":
        print(f"[ERROR] {orchestration.get('error')}")
        return

    print("[OK] Dataset successfully routed.")

    # ---------------------------------------------------------
    # 3. Clean Agent
    # ---------------------------------------------------------

    print("\n[3/4] Clean Agent")

    cleaning = clean_agent(file_path)

    if cleaning.get("status") != "success":
        print(f"[ERROR] {cleaning.get('error')}")
        return

    cleaned_file = cleaning["output_path"]

    print("[OK] Dataset cleaned successfully.")

    # ---------------------------------------------------------
    # 4. Analysis Agent
    # ---------------------------------------------------------

    print("\n[4/4] Analysis Agent")

    analysis = analysis_agent(
        cleaned_file,
        domain_config
    )

    if analysis.get("status") != "success":
        print(f"[ERROR] {analysis.get('error')}")
        return

    print("[OK] Analysis completed successfully.")

    # ---------------------------------------------------------
    # 5. Dynamic Dashboard Agent
    # ---------------------------------------------------------

    print("\n[5/5] Dynamic Dashboard Agent")

    dashboard = dashboard_agent(
        cleaned_file,
        analysis,
        domain_config
    )

    if dashboard.get("status") != "success":
        print(f"[ERROR] {dashboard.get('error')}")
        return

    print("[OK] Dashboard generated successfully.")

    # ---------------------------------------------------------
    # Final Result
    # ---------------------------------------------------------

    print("\n========================================")
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("========================================")

    print(f"\nDomain:\n{domain_config['domain']}")

    print("\nKey Metrics:")

    for key, value in analysis.get("metrics", {}).items():
        print(f"  {key}: {value}")

    print(f"\nCleaned Dataset:")
    print(f"  {cleaned_file}")

    print(f"\nAnalysis Report:")
    print(f"  {analysis['report_path']}")

    print(f"\nDashboard:")
    print(f"  {dashboard['dashboard_path']}")

    print("\nCharts:")

    for chart in dashboard["charts"]:
        print(f"  {chart}")


if __name__ == "__main__":
    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] Dataset not found: {DATASET_PATH}")
    else:
        run_pipeline(DATASET_PATH)