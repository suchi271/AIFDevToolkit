from pydantic import Field
from SorthaDevKit.StateBase import StateBase, ExcelOutputType

class State(StateBase):
    retry_count: int = 0
    retry_limit: int = 3
    questions: list[str] = Field(default=[], description="List of questions extracted from Excel file")
    transcript_content: str = Field(default='', description="Content of the transcript file")
    excel_output: ExcelOutputType = Field(default_factory=ExcelOutputType, description="Excel output data structure")
