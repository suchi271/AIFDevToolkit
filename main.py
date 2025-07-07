
from Workflows.CompleteMigrationPlan import CompleteMigrationPlanWorkflow
from State import State
from Input import Input
import sys
import logging
import os

# Suppress HTTP request logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)

# Set environment variable to reduce Azure SDK verbosity
os.environ.setdefault("AZURE_LOG_LEVEL", "WARNING")

def main():
    print("SorthaDevKit - Developer Toolkit")
    print("=" * 40)
    print("Running Complete Azure Migration Plan Generation (non-interactive)...")
    state = State(inputs=Input)
    workflow = CompleteMigrationPlanWorkflow(state)
    result = workflow.run()
    if result.success:
        print("\n✅ Complete migration plan generated successfully!")
    else:
        print("\n❌ Migration plan generation failed:")
        for error in result.errors:
            print(f"  - {error}")

if __name__ == "__main__":
    main()