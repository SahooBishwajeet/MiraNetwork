import os
import glob
from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
from typing import Dict, Any, Optional

def load_mira_client() -> MiraClient:
    load_dotenv()
    api_key = os.getenv("MIRA_API_KEY")
    if not api_key:
        raise ValueError("MIRA_API_KEY not found in environment")
    return MiraClient(config={"API_KEY": api_key})

def deploy_flows(client: MiraClient) -> None:
    flow_files = glob.glob("flows/*.yaml")

    for flow_file in flow_files:
        try:
            flow = Flow(source=flow_file)
            client.flow.deploy(flow)

            flow_name = os.path.splitext(os.path.basename(flow_file))[0]
            flow_id = f"void/{flow_name}"
            print(f"Flow deployed successfully: {flow_id}")

        except FlowError as e:
            print(f"Flow deployment error ({flow_file}): {e}")
        except Exception as e:
            print(f"Unexpected error deploying {flow_file}: {e}")

def test_flow(client: MiraClient, flow_id: str, inputs: Dict[str, Any]) -> Optional[Any]:
    try:
        return client.flow.execute(flow_id, inputs)
    except FlowError as e:
        print(f"Flow execution error: {e}")
        return None

def main():
    try:
        client = load_mira_client()

        print("Deploying flows...")
        deploy_flows(client)

        # Scenarios for different flows
        flows_to_test = {
            "mental-health-assistant": {
                "domain": "Comprehensive mental health support platform",
                "constraints": "HIPAA compliance, data privacy, secure user authentication",
                "scale": "1000 concurrent users, global accessibility"
            },
            "educational-personalization-engine": {
                "learning_style": "Visual",
                "academic_level": "High School",
                "subject_area": "Mathematics"
            },
            "climate-resilience-community-planner": {
                "region_type": "Coastal urban area",
                "population_density": 3500,
                "primary_climate_risk": "Sea level rise"
            }
        }

        # Test each flow
        for flow_name, inputs in flows_to_test.items():
            print(f"\nTesting {flow_name} flow...")
            result = test_flow(client, f"void/{flow_name}", inputs)

            if result:
                print(f"\n{flow_name.replace('-', ' ').title()} Response:")
                print(result)

    except Exception as e:
        print(f"Critical error in main execution: {e}")

if __name__ == "__main__":
    main()
