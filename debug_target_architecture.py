#!/usr/bin/env python3

import sys
import os
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SorthaDevKit.AssessmentReportGenerator import ApplicationAssessmentReportGenerator
from SorthaDevKit.ExcelUtils import ExcelProcessor
from Input import Input

def debug_target_architecture():
    """Debug target architecture generation and usage."""
    
    try:
        print("🔍 Debugging Target Architecture Generation")
        print("=" * 50)
        
        # Initialize components
        excel_processor = ExcelProcessor()
        assessment_generator = ApplicationAssessmentReportGenerator()
        
        # Process dependency analysis to get network connections
        print("📊 Processing dependency analysis...")
        dependency_analysis = excel_processor.read_dependency_analysis(Input["azmigrate_dependency_analysis"].file_path)
        print(f"✓ Found {len(dependency_analysis.connections)} network connections")
        
        # Process Azure Migrate data
        print("☁️ Processing Azure Migrate data...")
        azure_migrate_data = excel_processor.read_azure_migrate_report(Input["azure_migrate_report"].file_path)
        print(f"✓ Found {len(azure_migrate_data.servers)} servers")
        
        # Process questions
        print("❓ Processing questions...")
        questions_answers = excel_processor.read_questions_xlsx(Input["questions_excel"].file_path, Input["transcript"].file_path)
        print(f"✓ Processed {len(questions_answers)} questions")
        
        # Generate assessment report (this should create target_architecture)
        print("📋 Generating assessment report...")
        assessment_data = assessment_generator.generate_assessment_report(
            questions_answers=questions_answers,
            azure_migrate_data=azure_migrate_data,
            dependency_analysis=dependency_analysis,
            project_name="Debug Test Project"
        )
        
        print("✓ Assessment report generated")
        
        # Debug target architecture
        print("\n🏗️ Debugging Target Architecture:")
        if hasattr(assessment_data, 'target_architecture') and assessment_data.target_architecture:
            target_arch = assessment_data.target_architecture
            print(f"  Type: {type(target_arch)}")
            print(f"  Attributes: {dir(target_arch)}")
            
            # Check network connections
            if hasattr(target_arch, 'network_connections'):
                print(f"  Network Connections: {len(target_arch.network_connections)}")
                print(f"  Network Connections Type: {type(target_arch.network_connections)}")
            
            # Test the network analysis generation
            print("\n🧪 Testing network analysis generation...")
            try:
                network_analysis = assessment_generator._generate_comprehensive_network_analysis(target_arch)
                print("✓ Network analysis generated successfully")
                print(f"  Content length: {len(network_analysis)} characters")
                print(f"  First 200 chars: {network_analysis[:200]}...")
            except Exception as e:
                print(f"❌ Error in network analysis generation: {e}")
                print(f"   Exception type: {type(e)}")
                traceback.print_exc()
            
            # Test the format target architecture method
            print("\n🧪 Testing format target architecture...")
            try:
                formatted_content = assessment_generator._format_target_architecture_content("Production", target_arch)
                print("✓ Format target architecture successful")
                print(f"  Content length: {len(formatted_content)} characters")
            except Exception as e:
                print(f"❌ Error in format target architecture: {e}")
                print(f"   Exception type: {type(e)}")
                traceback.print_exc()
        else:
            print("❌ No target architecture found")
        
        # Test full Word export
        print("\n📄 Testing Word export...")
        try:
            success = assessment_generator.export_to_word(
                assessment_data=assessment_data,
                output_path="output/debug_assessment_report.docx"
            )
            if success:
                print("✓ Word export successful")
            else:
                print("❌ Word export failed")
        except Exception as e:
            print(f"❌ Error in Word export: {e}")
            print(f"   Exception type: {type(e)}")
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Debug script error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_target_architecture()
