#!/usr/bin/env python3
"""
Test script for enhanced assessment report generation with dependency analysis.
"""

import sys
import os
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SorthaDevKit.StateBase import QuestionAnswer, FileInputType
from SorthaDevKit.ExcelUtils import ExcelProcessor
from SorthaDevKit.AssessmentReportGenerator import ApplicationAssessmentReportGenerator
from Input import Input

def create_sample_qa_data() -> List[QuestionAnswer]:
    """Create sample Q&A data for testing."""
    sample_qa = [
        QuestionAnswer(
            question="What is the name of the application being migrated?",
            answer="CustomerPortal Web Application",
            confidence="High",
            is_answered=True,
            category="Application",
            priority="High",
            source_reference="Transcript"
        ),
        QuestionAnswer(
            question="What database technology does the application use?",
            answer="SQL Server 2019 with multiple databases for different modules",
            confidence="High",
            is_answered=True,
            category="Data",
            priority="High", 
            source_reference="Transcript"
        ),
        QuestionAnswer(
            question="Are there any external integrations?",
            answer="Yes, integrates with payment gateway, CRM system, and email service",
            confidence="Medium",
            is_answered=True,
            category="Integration",
            priority="Medium",
            source_reference="Transcript"
        ),
        QuestionAnswer(
            question="What are the current performance requirements?",
            answer="Supports 1000 concurrent users with response time under 2 seconds",
            confidence="Medium", 
            is_answered=True,
            category="Performance",
            priority="High",
            source_reference="Transcript"
        ),
        QuestionAnswer(
            question="What networking protocols are used?",
            answer="HTTPS for web traffic, JDBC for database connections, SMTP for email",
            confidence="Medium",
            is_answered=True,
            category="Network",
            priority="Medium",
            source_reference="Transcript"
        )
    ]
    return sample_qa

def test_enhanced_assessment_generation():
    """Test enhanced assessment report generation with dependency analysis."""
    print("Testing Enhanced Assessment Report Generation")
    print("=" * 50)
    
    try:
        # Get input files
        input_files = Input
        print(f"Found {len(input_files)} input files")
        
        # Create sample Q&A data
        questions_answers = create_sample_qa_data()
        print(f"Created {len(questions_answers)} sample Q&A pairs")
        
        # Load Azure Migrate data if available
        azure_migrate_data = None
        azure_migrate_input = input_files.get('azure_migrate_report')
        if azure_migrate_input and azure_migrate_input.file_path and os.path.exists(azure_migrate_input.file_path):
            try:
                azure_migrate_data = ExcelProcessor.read_azure_migrate_report(azure_migrate_input.file_path)
                if azure_migrate_data:
                    print(f"✓ Loaded Azure Migrate data with {len(azure_migrate_data.servers)} servers")
                else:
                    print("⚠ Failed to load Azure Migrate data")
            except Exception as e:
                print(f"⚠ Error loading Azure Migrate data: {e}")
        else:
            print("⚠ No Azure Migrate report found")
        
        # Load dependency analysis data if available  
        dependency_analysis = None
        dependency_input = input_files.get('azmigrate_dependency_analysis')
        if dependency_input and dependency_input.file_path and os.path.exists(dependency_input.file_path):
            try:
                dependency_analysis = ExcelProcessor.read_dependency_analysis(dependency_input.file_path)
                if dependency_analysis:
                    connection_count = len(dependency_analysis.connections) if dependency_analysis.connections else 0
                    segment_count = len(dependency_analysis.network_segments) if dependency_analysis.network_segments else 0
                    external_count = len(dependency_analysis.external_dependencies) if dependency_analysis.external_dependencies else 0
                    print(f"✓ Loaded dependency analysis: {connection_count} connections, {segment_count} segments, {external_count} external deps")
                else:
                    print("⚠ Failed to load dependency analysis data")
            except Exception as e:
                print(f"⚠ Error loading dependency analysis: {e}")
        else:
            print("⚠ No dependency analysis report found")
        
        # Create assessment report generator
        assessment_generator = ApplicationAssessmentReportGenerator()
        
        # Generate enhanced assessment report
        print("\nGenerating enhanced assessment report...")
        assessment_data = assessment_generator.generate_assessment_report(
            questions_answers=questions_answers,
            azure_migrate_data=azure_migrate_data,
            dependency_analysis=dependency_analysis,
            project_name="CustomerPortal Migration Project"
        )
        
        if assessment_data:
            print("✓ Successfully generated enhanced assessment report")
            
            # Display some key results
            print(f"Application Name: {assessment_data.application_name}")
            print(f"Security Considerations: {len(assessment_data.security_considerations)}")
            print(f"Network Requirements: {len(assessment_data.network_requirements)}")
            print(f"Architecture Heatmap: {len(assessment_data.architecture_heatmap)}")
            
            # Display network requirements to show enhancement
            print("\nNetwork Requirements (Enhanced with Dependency Analysis):")
            for i, req in enumerate(assessment_data.network_requirements[:5], 1):
                print(f"  {i}. {req.get('category', 'Unknown')}: {req.get('requirement', 'N/A')[:100]}...")
                if 'source' in req:
                    print(f"      Source: {req['source']}")
            
            # Display architecture heatmap to show complexity analysis
            print("\nArchitecture Complexity Heatmap:")
            for item in assessment_data.architecture_heatmap:
                print(f"  - {item.get('area', 'Unknown')}: {item.get('ranking', 'Unknown')} complexity")
                print(f"    {item.get('notes', 'No details')[:80]}...")
            
            return True
        else:
            print("✗ Failed to generate assessment report")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_assessment_generation()
    if success:
        print("\n✓ Enhanced assessment report generation test completed successfully!")
    else:
        print("\n✗ Enhanced assessment report generation test failed!")
        sys.exit(1)
