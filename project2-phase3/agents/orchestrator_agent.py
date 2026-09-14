import pandas as pd


def orchestrator_agent(file_path, domain_config):
    """
    Routes the configured dataset through the production pipeline.

    Pipeline:
    Domain Configuration
        ↓
    Clean Agent
        ↓
    Analysis Agent
        ↓
    Dashboard Agent
    """

    try:
        # Validate the dataset before routing
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        print("\n[Orchestrator] Pipeline started.")
        print(f"[Orchestrator] Dataset rows: {len(df)}")
        print(f"[Orchestrator] Dataset columns: {len(df.columns)}")

        if domain_config.get("error"):
            print("[Orchestrator] Domain configuration contains an error.")
            return {
                "status": "failed",
                "error": domain_config["error"]
            }

        print("[Orchestrator] Domain configuration received.")
        print("[Orchestrator] Routing dataset to Clean Agent...")

        return {
            "status": "ready",
            "file_path": file_path,
            "domain_config": domain_config,
            "message": "Dataset successfully routed to the Clean Agent."
        }

    except FileNotFoundError:
        return {
            "status": "failed",
            "error": f"Dataset not found: {file_path}"
        }

    except pd.errors.EmptyDataError:
        return {
            "status": "failed",
            "error": "The dataset is empty or unreadable."
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Orchestrator failed: {str(e)}"
        }
