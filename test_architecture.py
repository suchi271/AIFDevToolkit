"""
Test script for Azure Migrate report processing and architecture diagram generation
===================================================================================

This script tests the new functionality without requiring the full workflow.
Use this to validate Azure Migrate report parsing and diagram generation.
"""

import os
import sys
from datetime import datetime

def test_azure_migrate_processing():
    """Test Azure Migrate report processing independently."""
    print("Testing Azure Migrate Report Processing")
    print("=" * 50)
    
    try:
        # Add the project root to path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from SorthaDevKit.ExcelUtils import ExcelProcessor
        from SorthaDevKit.ArchitectureDiagram import ArchitectureDiagramGenerator
        from SorthaDevKit.StateBase import ExcelOutputType, QuestionAnswer
        from Input import Input, OUTPUT_CONFIG
        
        # Test Azure Migrate report processing
        migrate_report_path = Input['azure_migrate_report'].file_path
        
        if not os.path.exists(migrate_report_path):
            print(f"❌ Azure Migrate report not found: {migrate_report_path}")
            print("Please ensure the file exists and try again.")
            return False
        
        print(f"📁 Processing: {os.path.basename(migrate_report_path)}")
        
        # Parse the Azure Migrate report
        migrate_report = ExcelProcessor.read_azure_migrate_report(migrate_report_path)
        
        print(f"✅ Successfully parsed Azure Migrate report")
        print(f"📊 Servers found: {len(migrate_report.servers)}")
        print(f"📋 Sheets processed: {migrate_report.metadata.get('sheets_processed', [])}")
        
        # Display server summary
        if migrate_report.servers:
            print("\n🖥️  Server Summary:")
            for i, server in enumerate(migrate_report.servers[:5]):  # Show first 5
                print(f"   {i+1}. {server.server_name}")
                print(f"      OS: {server.operating_system}")
                print(f"      CPU: {server.cpu_cores} cores, RAM: {server.memory_gb} GB")
                print(f"      Recommendation: {server.recommendation}")
                print()
            
            if len(migrate_report.servers) > 5:
                print(f"   ... and {len(migrate_report.servers) - 5} more servers")
        
        # Test architecture diagram generation with sample Q&A
        print("🏗️  Testing Architecture Diagram Generation...")
        
        # Create sample Q&A data for testing
        sample_qa = ExcelOutputType(
            questions_answers=[
                QuestionAnswer(
                    question="What technologies are currently in use?",
                    answer="We have SQL Server databases, IIS web servers, and some Docker containers for microservices.",
                    confidence="High",
                    is_answered=True
                ),
                QuestionAnswer(
                    question="What are the performance requirements?",
                    answer="Need to handle 10,000 concurrent users with high availability.",
                    confidence="Medium",
                    is_answered=True
                ),
                QuestionAnswer(
                    question="Are there any compliance requirements?",
                    answer="Yes, we need GDPR compliance and data encryption at rest.",
                    confidence="High",
                    is_answered=True
                )
            ]
        )
        
        # Generate architecture diagram
        diagram_generator = ArchitectureDiagramGenerator()
        architecture_diagram = diagram_generator.generate_architecture_from_migrate_and_transcript(
            migrate_report, sample_qa
        )
        
        print(f"✅ Generated architecture diagram")
        print(f"🔧 Components created: {len(architecture_diagram.components)}")
        
        # Display component summary
        if architecture_diagram.components:
            print("\n🏛️  Architecture Components:")
            tier_summary = {}
            for component in architecture_diagram.components:
                tier = component.tier
                if tier not in tier_summary:
                    tier_summary[tier] = []
                tier_summary[tier].append(component)
            
            for tier, components in tier_summary.items():
                print(f"   {tier.title()} Tier: {len(components)} components")
                for comp in components[:3]:  # Show first 3 per tier
                    print(f"      - {comp.name} ({comp.azure_service})")
                if len(components) > 3:
                    print(f"      ... and {len(components) - 3} more")
                print()
        
        # Test export functionality
        print("💾 Testing Export Functionality...")
        
        output_dir = os.path.dirname(OUTPUT_CONFIG['output_file_path'])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        test_outputs = {
            'JSON': OUTPUT_CONFIG['architecture_diagram_json'].replace('.json', '_test.json'),
            'SVG': OUTPUT_CONFIG['architecture_diagram_svg'].replace('.svg', '_test.svg'),
            'XML': OUTPUT_CONFIG['architecture_diagram_xml'].replace('.xml', '_test.xml'),
            'VSDX': OUTPUT_CONFIG['architecture_diagram_vsdx'].replace('.vsdx', '_test.vsdx')
        }
        
        # Export in different formats
        diagram_generator.export_to_json(architecture_diagram, test_outputs['JSON'])
        diagram_generator.export_to_svg(architecture_diagram, test_outputs['SVG'])
        diagram_generator.export_to_visio_xml(architecture_diagram, test_outputs['XML'])
        diagram_generator.export_to_visio_vsdx(architecture_diagram, test_outputs['VSDX'])
        
        print("✅ Successfully exported diagrams:")
        for format_name, file_path in test_outputs.items():
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            print(f"   📄 {format_name}: {os.path.basename(file_path)} ({file_size} bytes)")
        
        print("\n🎉 All tests passed successfully!")
        print("\n📝 Next Steps:")
        print("   1. Review the test output files in the output directory")
        print("   2. Try opening the VSDX file directly in Visio")
        print("   3. Try opening the SVG file in a web browser")
        print("   4. Run the full enhanced workflow: python main.py 2")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required modules are available.")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_azure_migrate_processing()
