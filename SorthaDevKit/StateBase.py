from pydantic import BaseModel, Field
from typing import Union, List, Dict, Any, Optional
from enum import StrEnum
from datetime import datetime

class FileTypes(StrEnum):
    TEXT = 'text'
    EXCEL = 'excel'
    UNDEFINED = 'undefined'

class FileInputType(BaseModel):
    type: FileTypes = Field(default=FileTypes.UNDEFINED, description="Type of input, e.g. 'text', 'file', etc.")
    file_path: str = Field(default='', description="Path to the file input")
    content: str = Field(default='', description="Content of the input, e.g. text or file content")

class UserInputType(BaseModel):
    content: str = Field(default='', description="Content of the input, e.g. text or file content")

class StateBase(BaseModel):
    inputs: dict[str, Union[FileInputType, UserInputType]] = Field(default={}, description="Dictionary of inputs")
    output: str = Field(default='', description="Output of the workflow")

class QuestionAnswer(BaseModel):
    """Data model for a question-answer pair."""
    question: str
    answer: str = ""
    confidence: str = "Medium"
    source_reference: str = ""
    is_answered: bool = False
    category: str = ""
    priority: str = "Medium"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ExcelOutputType(BaseModel):
    """Data model for Excel output structure."""
    questions_answers: List[QuestionAnswer] = Field(default_factory=list)
    unanswered_questions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    summary: Dict[str, Any] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    """Base state class for workflow operations."""
    current_step: str = ""
    progress: float = 0.0
    status: str = "initialized"
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_error(self, error: str):
        """Add an error to the state."""
        self.errors.append(error)
        self.status = "error"
    
    def set_progress(self, progress: float, step: str = ""):
        """Update progress and current step."""
        self.progress = max(0.0, min(100.0, progress))
        if step:
            self.current_step = step
        
        if self.progress >= 100.0:
            self.status = "completed"
        elif self.progress > 0:
            self.status = "running"

class ProcessingResult(BaseModel):
    """Result of a processing operation."""
    success: bool = False
    message: str = ""
    data: Any = None
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_error(self, error: str):
        """Add an error to the result."""
        self.errors.append(error)
        self.success = False
    
    def set_success(self, message: str = "", data: Any = None):
        """Mark the result as successful."""
        self.success = True
        if message:
            self.message = message
        if data is not None:
            self.data = data