"""
Enhanced AIF Completion with Architecture Diagram Generation
============================================================

Enhanced workflow that processes Azure Migrate reports and generates architecture diagrams
alongside the existing AIF completion functionality.
"""
import os
import sys
from datetime import datetime

def main():
    print("Enhanced SorthaDevKit AIF Completion with Architecture Diagram")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        print("Loading modules...")
        from Workflow import QuestionAnsweringWorkFlow
        from State import State
        from Input import Input, OUTPUT_CONFIG
        from Config import LLMConfig
        from langchain_openai import AzureChatOpenAI
        from SorthaDevKit.ExcelUtils import ExcelProcessor
        from SorthaDevKit.ArchitectureDiagram import ArchitectureDiagramGenerator
        print("✓ Modules loaded")
        
        # Validate input files
        print("Validating inputs...")
        transcript_path = Input['transcript'].file_path
        questions_path = Input['questions_excel'].file_path
        migrate_report_path = Input['azure_migrate_report'].file_path
        
        if not os.path.exists(transcript_path):
            print(f"✗ Transcript not found: {transcript_path}")
            return False
            
        if not os.path.exists(questions_path):
            print(f"✗ Input AIF file not found: {questions_path}")
            return False
            
        if not os.path.exists(migrate_report_path):
            print(f"✗ Azure Migrate report not found: {migrate_report_path}")
            return False
            
        print("✓ Input files validated")
        
        # Initialize Azure OpenAI
        print("Connecting to Azure OpenAI...")
        llm = AzureChatOpenAI(
            deployment_name=LLMConfig.AZURE_OPENAI_DEPLOYMENT_NAME,
            model_name=LLMConfig.AZURE_OPENAI_MODEL_NAME,
            temperature=LLMConfig.AZURE_OPENAI_TEMPERATURE,
            api_key=LLMConfig.AZURE_OPENAI_API_KEY,
            azure_endpoint=LLMConfig.AZURE_OPENAI_ENDPOINT,
            api_version=LLMConfig.AZURE_OPENAI_API_VERSION
        )
        print(f"✓ Connected to {LLMConfig.AZURE_OPENAI_MODEL_NAME}")
        
        # Process Azure Migrate Report
        print("Processing Azure Migrate report...")
        migrate_report = ExcelProcessor.read_azure_migrate_report(migrate_report_path)
        print(f"✓ Processed {len(migrate_report.servers)} servers from Azure Migrate report")
        
        # Setup and execute Q&A workflow
        print("Processing questions...")
        workflow = QuestionAnsweringWorkFlow(llm)
        initial_state = State(inputs=Input)
        
        workflow.createStateGraph(State)
        workflow.buildGraph()
        
        result = workflow.invoke(initial_state)
        
        # Process Q&A results
        if hasattr(result, 'excel_output'):
            excel_output = result.excel_output
        else:
            excel_output = None
        
        if not excel_output or not excel_output.questions_answers:
            print("✗ No Q&A results generated")
            return False
        
        # Generate Excel report (existing functionality)
        output_path = OUTPUT_CONFIG.get('output_file_path', 'output/filled_aif.xlsx')
        output_dir = os.path.dirname(output_path)
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        ExcelProcessor.create_output_excel(excel_output, output_path, questions_path)
        
        # Generate Architecture Diagram
        print("Generating architecture diagram...")
        diagram_generator = ArchitectureDiagramGenerator()
        architecture_diagram = diagram_generator.generate_architecture_from_migrate_and_transcript(
            migrate_report, excel_output
        )
        print(f"✓ Generated architecture with {len(architecture_diagram.components)} components")
        
        # Export architecture diagram in multiple formats
        print("Exporting architecture diagrams...")
        
        # JSON format
        json_path = OUTPUT_CONFIG.get('architecture_diagram_json', 'output/architecture_diagram.json')
        diagram_generator.export_to_json(architecture_diagram, json_path)
        print(f"✓ JSON diagram saved: {json_path}")
        
        # VSDX format (Native Visio format)
        vsdx_path = OUTPUT_CONFIG.get('architecture_diagram_vsdx', 'output/architecture_diagram.vsdx')
        diagram_generator.export_to_visio_vsdx(architecture_diagram, vsdx_path)
        print(f"✓ VSDX diagram saved: {vsdx_path}")
        
        # SVG format (Visio-importable)
        svg_path = OUTPUT_CONFIG.get('architecture_diagram_svg', 'output/architecture_diagram.svg')
        diagram_generator.export_to_svg(architecture_diagram, svg_path)
        print(f"✓ SVG diagram saved: {svg_path}")
        
        # Enhanced XML format (Visio-compatible)
        xml_path = OUTPUT_CONFIG.get('architecture_diagram_xml', 'output/architecture_diagram.xml')
        diagram_generator.export_to_visio_xml(architecture_diagram, xml_path)
        print(f"✓ Enhanced Visio XML diagram saved: {xml_path}")
        
        # Display results
        total_qa = len(excel_output.questions_answers)
        answered_qa = len([qa for qa in excel_output.questions_answers if qa.is_answered])
        total_servers = len(migrate_report.servers)
        total_components = len(architecture_diagram.components)
        
        print()
        print("🎉 Processing complete!")
        print(f"📋 Q&A Processing:")
        print(f"   Questions processed: {total_qa}")
        print(f"   Questions answered: {answered_qa}")
        print(f"   Answer rate: {(answered_qa/total_qa*100):.1f}%")
        print(f"   Report saved: {output_path}")
        
        print(f"🏗️  Architecture Diagram:")
        print(f"   Source servers: {total_servers}")
        print(f"   Azure components: {total_components}")
        print(f"   Diagram formats: VSDX, JSON, SVG, XML")
        
        print(f"📁 Output files:")
        print(f"   Excel Report: {output_path}")
        print(f"   Architecture VSDX: {vsdx_path}")
        print(f"   Architecture JSON: {json_path}")
        print(f"   Architecture SVG: {svg_path}")
        print(f"   Architecture XML: {xml_path}")
        
        print()
        print("📝 Next Steps:")
        print("   1. Review the filled AIF Excel report")
        print("   2. Open the VSDX file directly in Visio for full editing")
        print("   3. Use the SVG file for web viewing or import into other tools")
        print("   4. Use the JSON file for programmatic access")
        print("   5. Customize the architecture as needed")
        
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
