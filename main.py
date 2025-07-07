
from Workflows import FilledAIF, EnhancedFilledAIF
import sys

def main():
    print("SorthaDevKit - Developer Toolkit")
    print("=" * 40)
    print("Available workflows:")
    print("1. Standard AIF Completion (existing functionality)")
    print("2. Enhanced AIF Completion with Architecture Diagram")
    print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Select workflow (1 or 2, default: 2): ").strip()
        if not choice:
            choice = "2"
    
    if choice == "1":
        print("Running Standard AIF Completion...")
        FilledAIF.main()
    else:
        print("Running Enhanced AIF Completion with Architecture Diagram...")
        EnhancedFilledAIF.main()

if __name__ == "__main__":
    main()