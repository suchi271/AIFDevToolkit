"""
SorthaDevKit AIF Completion
=====================================

Execution script for AI-powered transcript analysis and AIF Filling.
"""
import os
import sys
from datetime import datetime

def main():
    print("SorthaDevKit AIF Completion")
    print("=" * 60)
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
        print("✓ Modules loaded")
        
        # Validate input files
        print("Validating inputs...")
        transcript_path = Input['transcript'].file_path
        questions_path = Input['questions_excel'].file_path
        
        if not os.path.exists(transcript_path):
            print(f"✗ Transcript not found: {transcript_path}")
            return False
            
        if not os.path.exists(questions_path):
            print(f"✗ Input AIF file not found: {questions_path}")
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
        
        # Setup and execute workflow
        print("Processing questions...")
        workflow = QuestionAnsweringWorkFlow(llm)
        initial_state = State(inputs=Input)
        
        workflow.createStateGraph(State)
        workflow.buildGraph()
        
        result = workflow.invoke(initial_state)
        
        # Process results
        if hasattr(result, 'excel_output'):
            excel_output = result.excel_output
        else:
            excel_output = None
        
        if not excel_output or not excel_output.questions_answers:
            print("✗ No results generated")
            return False
        
        # Generate Excel report
        output_path = OUTPUT_CONFIG.get('output_file_path', 'output/filled_aif.xlsx')
        output_dir = os.path.dirname(output_path)
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        ExcelProcessor.create_output_excel(excel_output, output_path, questions_path)
        
        # Display results
        total = len(excel_output.questions_answers)
        answered = len([qa for qa in excel_output.questions_answers if qa.is_answered])
        
        print(f"✓ Processing complete!")
        print(f"  Questions processed: {total}")
        print(f"  Questions answered: {answered}")
        print(f"  Answer rate: {(answered/total*100):.1f}%")
        print(f"  Report saved: {output_path}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
