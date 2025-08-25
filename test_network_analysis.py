#!/usr/bin/env python3
"""
Test script to show the network analysis output format
This demonstrates what the 221 parsed connections are being used for
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SorthaDevKit.ExcelUtils import ExcelProcessor
from SorthaDevKit.AssessmentReportGenerator import ApplicationAssessmentReportGenerator
from Input import Input

def test_network_analysis_output():
    """Test and display the network analysis output format"""
    
    print("🔍 NETWORK ANALYSIS OUTPUT TEST")
    print("=" * 50)
    
    try:
        # Load dependency analysis data directly
        excel_utils = ExcelProcessor()
        dependency_file = Input["azmigrate_dependency_analysis"].file_path
        print(f"📊 Loading dependency analysis from: {dependency_file}")
        
        dependency_analysis = excel_utils.read_dependency_analysis(dependency_file)
        
        print(f"✓ Loaded {len(dependency_analysis.connections)} dependency connections")
        print()
        
        # Generate target architecture
        generator = ApplicationAssessmentReportGenerator()
        target_architecture = generator._generate_target_architecture(
            [], None, dependency_analysis  # Empty Q&A and Azure Migrate for this test
        )
        
        print(f"✓ Generated target architecture with:")
        print(f"  - {len(target_architecture.network_connections)} network connections")
        print(f"  - {len(target_architecture.subnet_recommendations)} subnet recommendations") 
        print(f"  - {len(target_architecture.nsg_rules)} NSG rules")
        print(f"  - {len(target_architecture.load_balancer_config)} load balancer configs")
        print()
        
        # Show sample connection data
        print("📋 SAMPLE CONNECTION DATA (first 5 connections):")
        print("-" * 60)
        for i, conn in enumerate(target_architecture.network_connections[:5]):
            print(f"Connection {i+1}:")
            print(f"  Source: {conn.source_ip} ({conn.source_application})")
            print(f"  Destination: {conn.destination_ip}:{conn.destination_port} ({conn.destination_application})")
            print()
        
        # Generate the formatted output
        print("🎯 FORMATTED NETWORK ANALYSIS OUTPUT:")
        print("-" * 50)
        
        formatted_output = generator._generate_comprehensive_network_analysis(target_architecture)
        print(formatted_output)
        
        print()
        print("💡 This exact output is now included in the Word documents!")
        print("   Check: output/application_assessment_report.docx")
        print("   Section: 'Proposed Architecture in Azure'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_network_analysis_output()
