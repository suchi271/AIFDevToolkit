from SorthaDevKit.WorkFlowBase import QuestionAnsweringWorkFlowBase
from SorthaDevKit.StateBase import QuestionAnswer, ExcelOutputType, ProcessingResult
from State import State
from Input import OUTPUT_CONFIG
import os
import logging
from typing import Dict, Any

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)

class QuestionAnsweringWorkFlow(QuestionAnsweringWorkFlowBase):

    def __init__(self, llm=None):
        """Initialize the workflow with optional LLM."""
        super().__init__("QuestionAnsweringWorkFlow")
        if llm:
            self._llm = llm
            self.llm_client = llm  # Set base class attribute too
    
    def invoke(self, initial_state):
        """Invoke the workflow with initial state."""
        try:
            # Execute the workflow steps in order
            state = self.load_inputs(initial_state)
            if "Error" not in state.output:
                state = self.process_questions(state)
                if "Error" not in state.output:
                    state = self.generate_output(state)
            
            return state
        except Exception as e:
            initial_state.output = f"Error in workflow: {str(e)}"
            return initial_state
    
    def load_inputs(self, state: State) -> State:
        try:
            # Load transcript content using base class method
            if 'transcript' in state.inputs:
                transcript_input = state.inputs['transcript']
                if transcript_input.file_path and os.path.exists(transcript_input.file_path):
                    if self.load_transcript_from_file(transcript_input.file_path):
                        state.transcript_content = self.transcript_content
                        transcript_input.content = state.transcript_content
                    else:
                        state.output = "Error loading transcript file"
                        return state
                else:
                    self.transcript_content = transcript_input.content
                    state.transcript_content = transcript_input.content
            
            # Load questions from Excel using base class method
            if 'questions_excel' in state.inputs:
                excel_input = state.inputs['questions_excel']
                if excel_input.file_path and os.path.exists(excel_input.file_path):
                    if self.load_questions_from_excel(
                        excel_input.file_path,
                        question_column=OUTPUT_CONFIG.get('question_column_name', 'Question'),
                        sheet_name=OUTPUT_CONFIG.get('excel_sheet_name')
                    ):
                        state.questions = self.questions
                        excel_input.content = f"Loaded {len(self.questions)} questions from Excel file"
                    else:
                        state.output = "Error loading questions from Excel"
                        return state
                else:
                    raise FileNotFoundError(f"Excel file not found: {excel_input.file_path}")
            
            print(f"✓ Loaded transcript ({len(state.transcript_content)} chars) and {len(state.questions)} questions")
            return state
            
        except Exception as e:
            state.output = f"Error loading inputs: {str(e)}"
            return state
    
    def process_questions(self, state: State) -> State:
        """Process each question against the transcript using base class methods."""
        if not state.questions or not state.transcript_content:
            state.output = "Missing questions or transcript content"
            return state
        
        try:
            # Set up the transcript in the base class
            self.transcript_content = state.transcript_content
            
            # Process all questions using base class method
            questions_answers = self.process_all_questions(state.questions)
            
            if not questions_answers:
                state.output = "No questions were processed successfully"
                return state
            
            # Identify unanswered questions
            unanswered = [qa.question for qa in questions_answers if not qa.is_answered]
            
            # Update state with results
            state.excel_output = ExcelOutputType(
                questions_answers=questions_answers,
                unanswered_questions=unanswered,
                summary={
                    "total_questions": len(state.questions),
                    "answered_questions": len([qa for qa in questions_answers if qa.is_answered]),
                    "processing_status": "completed"
                }
            )
            
            return state
            
        except Exception as e:
            state.output = f"Error processing questions: {str(e)}"
            return state
    
    def generate_output(self, state: State) -> State:
        """Generate Excel output file with answers using base class methods."""
        try:
            # Get output path and original file path
            output_path = OUTPUT_CONFIG.get('output_file_path', 'output/filled_aif.xlsx')
            excel_input = state.inputs.get('questions_excel')
            original_file_path = excel_input.file_path if excel_input else None
            
            # Use base class method to create Excel output
            if self.create_excel_output(state.excel_output.questions_answers, output_path, original_file_path):
                # Generate summary using base class method
                summary = self.get_processing_summary(state.excel_output.questions_answers)
                
                state.output = f"""
Question-Answering Analysis Complete!

Summary:
- Total Questions: {summary['total_questions']}
- Answered Questions: {summary['answered_questions']}
- Unanswered Questions: {summary['unanswered_questions']}
- Answer Rate: {summary['answer_rate_percent']:.1f}%

Output saved to: {output_path}

Confidence Distribution:
- High: {summary['confidence_distribution'].get('High', 0)}
- Medium: {summary['confidence_distribution'].get('Medium', 0)}
- Low: {summary['confidence_distribution'].get('Low', 0)}
- Unknown: {summary['confidence_distribution'].get('Unknown', 0)}
"""
            else:
                state.output = "Error: Failed to create Excel output"
            
            return state
            
        except Exception as e:
            state.output = f"Error generating output: {str(e)}"
            return state
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the workflow with configuration using base class methods."""
        try:
            # Initialize LLM if not already done
            if not hasattr(self, '_llm') or not self._llm:
                from Config import LLMConfig
                
                llm_config = {
                    'AZURE_OPENAI_DEPLOYMENT_NAME': LLMConfig.AZURE_OPENAI_DEPLOYMENT_NAME,
                    'AZURE_OPENAI_MODEL_NAME': LLMConfig.AZURE_OPENAI_MODEL_NAME,
                    'AZURE_OPENAI_TEMPERATURE': LLMConfig.AZURE_OPENAI_TEMPERATURE,
                    'AZURE_OPENAI_API_KEY': LLMConfig.AZURE_OPENAI_API_KEY,
                    'AZURE_OPENAI_ENDPOINT': LLMConfig.AZURE_OPENAI_ENDPOINT,
                    'AZURE_OPENAI_API_VERSION': LLMConfig.AZURE_OPENAI_API_VERSION
                }
                
                if self.initialize_llm(llm_config):
                    self._llm = self.llm_client
                else:
                    return False
            
            return True
        except Exception as e:
            print(f"Failed to initialize workflow: {str(e)}")
            return False
    
    def buildGraph(self):
        self.getStateGraph().add_node("load_inputs", self.load_inputs)
        self.getStateGraph().add_node("process_questions", self.process_questions)
        self.getStateGraph().add_node("generate_output", self.generate_output)
        
        self.getStateGraph().add_edge(self.getStartNodePointer(), "load_inputs")
        self.getStateGraph().add_edge("load_inputs", "process_questions")
        self.getStateGraph().add_edge("process_questions", "generate_output")
        self.getStateGraph().add_edge("generate_output", self.getEndNodePointer())

    def execute(self, input_data: Any) -> ProcessingResult:
        """Execute the main workflow logic."""
        try:
            # Create state from input data
            if hasattr(input_data, 'inputs'):
                state = input_data
            else:
                from State import State
                state = State(inputs=input_data)
            
            # Execute workflow steps
            state = self.load_inputs(state)
            if "Error" in state.output:
                result = ProcessingResult()
                result.add_error(state.output)
                return result
            
            state = self.process_questions(state)
            if "Error" in state.output:
                result = ProcessingResult()
                result.add_error(state.output)
                return result
            
            state = self.generate_output(state)
            if "Error" in state.output:
                result = ProcessingResult()
                result.add_error(state.output)
                return result
            
            # Success
            result = ProcessingResult()
            result.success = True
            result.output = state.output
            return result
            
        except Exception as e:
            result = ProcessingResult()
            result.add_error(f"Execution failed: {str(e)}")
            return result
    
    def cleanup(self) -> bool:
        """Clean up resources after workflow execution."""
        try:
            # Clean up any resources if needed
            return True
        except Exception as e:
            print(f"Cleanup failed: {str(e)}")
            return False
    
    def getLLM(self):
        """Get the LLM instance."""
        if not hasattr(self, '_llm') or not self._llm:
            self.initialize({})
        return self._llm
