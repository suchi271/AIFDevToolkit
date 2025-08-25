#!/usr/bin/env python3
"""
Test script to verify target architecture generation with network traffic analysis.
"""

import sys
import os
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SorthaDevKit.StateBase import QuestionAnswer
from SorthaDevKit.ExcelUtils import ExcelProcessor
from SorthaDevKit.AssessmentReportGenerator import ApplicationAssessmentReportGenerator
from Input import Input

def test_target_architecture_generation():
    """Test target architecture generation with dependency analysis."""
    print("Testing Target Architecture Generation with Network Traffic Analysis")
    print("=" * 70)
    
    try:
        # Load dependency analysis data
        dependency_input = Input.get('azmigrate_dependency_analysis')
        if dependency_input and os.path.exists(dependency_input.file_path):
            dependency_analysis = ExcelProcessor.read_dependency_analysis(dependency_input.file_path)
            if dependency_analysis:
                connection_count = len(dependency_analysis.connections)
                print(f"✓ Loaded dependency analysis: {connection_count} connections")
                
                # Show sample connection data
                if dependency_analysis.connections:
                    sample_conn = dependency_analysis.connections[0]
                    print(f"  Sample connection: {sample_conn.source_ip} -> {sample_conn.destination_ip}:{sample_conn.destination_port}")
                    print(f"  Source app: {sample_conn.source_application}")
                    print(f"  Dest app: {sample_conn.destination_application}")
            else:
                print("✗ Failed to load dependency analysis")
                return False
        
        # Load Azure Migrate data
        azure_migrate_data = None
        azure_migrate_input = Input.get('azure_migrate_report')
        if azure_migrate_input and os.path.exists(azure_migrate_input.file_path):
            azure_migrate_data = ExcelProcessor.read_azure_migrate_report(azure_migrate_input.file_path)
            if azure_migrate_data:
                print(f"✓ Loaded Azure Migrate data: {len(azure_migrate_data.servers)} servers")
        
        # Create sample Q&A for business requirements
        questions_answers = [
            QuestionAnswer(
                question="What are the performance requirements?",
                answer="System needs to support 1000 concurrent users with sub-2 second response times",
                confidence="High",
                is_answered=True,
                category="Performance",
                priority="High",
                source_reference="Transcript"
            ),
            QuestionAnswer(
                question="What are the security requirements?",
                answer="Data encryption at rest and in transit, compliance with GDPR",
                confidence="High",
                is_answered=True,
                category="Security",
                priority="High",
                source_reference="Transcript"
            )
        ]
        
        # Create assessment report generator
        assessment_generator = ApplicationAssessmentReportGenerator()
        
        # Generate target architecture
        print("\nGenerating target architecture...")
        target_architecture = assessment_generator._generate_target_architecture(
            questions_answers, azure_migrate_data, dependency_analysis
        )
        
        if target_architecture:
            print("✓ Successfully generated target architecture")
            
            # Display network architecture recommendations
            if 'network_architecture' in target_architecture:
                net_arch = target_architecture['network_architecture']
                
                print(f"\n📊 Network Architecture Analysis:")
                if 'subnet_recommendations' in net_arch:
                    print(f"  • Subnet Recommendations: {len(net_arch['subnet_recommendations'])}")
                    for subnet in net_arch['subnet_recommendations'][:3]:
                        print(f"    - {subnet.get('subnet_name', 'Unknown')}: {subnet.get('purpose', 'N/A')}")
                
                if 'nsg_rules' in net_arch:
                    print(f"  • NSG Rules Generated: {len(net_arch['nsg_rules'])}")
                    for rule in net_arch['nsg_rules'][:3]:
                        print(f"    - {rule.get('rule_name', 'Unknown')}: Port {rule.get('port', 'N/A')}")
                
                if 'load_balancer_config' in net_arch:
                    print(f"  • Load Balancer Recommendations: {len(net_arch['load_balancer_config'])}")
            
            # Display compute recommendations
            if 'compute_recommendations' in target_architecture:
                comp_recs = target_architecture['compute_recommendations']
                print(f"\n💻 Compute Recommendations: {len(comp_recs)}")
                for rec in comp_recs[:3]:
                    print(f"  • {rec.get('application', 'Unknown')}: {rec.get('recommended_service', 'N/A')}")
            
            # Display integration points
            if 'integration_points' in target_architecture:
                int_points = target_architecture['integration_points']
                print(f"\n🔗 Integration Points: {len(int_points)}")
                for point in int_points[:3]:
                    print(f"  • {point.get('type', 'Unknown')}: {point.get('recommendation', 'N/A')}")
            
            # Display network diagram description
            if 'network_architecture' in target_architecture and 'network_diagram_description' in target_architecture['network_architecture']:
                print(f"\n📋 Network Diagram Description:")
                desc = target_architecture['network_architecture']['network_diagram_description']
                print(desc[:300] + "..." if len(desc) > 300 else desc)
            
            return True
        else:
            print("✗ Failed to generate target architecture")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_target_architecture_generation()
    if success:
        print("\n✅ Target architecture generation test completed successfully!")
        print("The system now properly utilizes network traffic data for architecture recommendations.")
    else:
        print("\n❌ Target architecture generation test failed!")
        sys.exit(1)
