import pandas as pd
import openpyxl
from typing import List, Dict, Any
from .StateBase import QuestionAnswer, ExcelOutputType
import os
from datetime import datetime

class ExcelProcessor:
    """Utility class for processing Excel files with questions and generating output Excel files."""
    
    @staticmethod
    def read_questions_from_excel(file_path: str, question_column: str = 'Question', sheet_name: str = None) -> List[str]:
        """
        Read questions from an Excel file.
        
        Args:
            file_path: Path to the Excel file
            question_column: Name of the column containing questions
            sheet_name: Name of the sheet to read (None for first sheet)
            
        Returns:
            List of questions
        """
        try:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            possible_columns = [question_column, 'Questions', 'Question', 'questions', 'QUESTION']
            question_col = None
            
            for col in possible_columns:
                if col in df.columns:
                    question_col = col
                    break
            
            if question_col is None:
                question_col = df.columns[0]
            
            questions = df[question_col].dropna().tolist()
            return [str(q).strip() for q in questions if str(q).strip()]
            
        except Exception as e:
            raise Exception(f"Error reading Excel file {file_path}: {str(e)}")
    
    @staticmethod
    def create_output_excel(excel_output: ExcelOutputType, output_path: str, original_questions_file: str = None):
        """
        Create an Excel file with questions, answers, and analysis.
        
        Args:
            excel_output: ExcelOutputType object with processed data
            output_path: Path where to save the output Excel file
            original_questions_file: Path to original questions file for reference
        """
        try:
            wb = openpyxl.Workbook()
            ws_qa = wb.active
            ws_qa.title = "AI Assisted AIF Completion"
            headers = ['Question', 'Answer', 'Confidence', 'Source Reference', 'Status']
            for col, header in enumerate(headers, 1):
                ws_qa.cell(row=1, column=col, value=header)
                ws_qa.cell(row=1, column=col).font = openpyxl.styles.Font(bold=True)
            for row, qa in enumerate(excel_output.questions_answers, 2):
                ws_qa.cell(row=row, column=1, value=qa.question)
                ws_qa.cell(row=row, column=2, value=qa.answer)
                ws_qa.cell(row=row, column=3, value=qa.confidence)
                ws_qa.cell(row=row, column=4, value=qa.source_reference)
                ws_qa.cell(row=row, column=5, value="Answered" if qa.is_answered else "Not Answered")
                
                if qa.confidence == "High":
                    ws_qa.cell(row=row, column=3).fill = openpyxl.styles.PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
                elif qa.confidence == "Medium":
                    ws_qa.cell(row=row, column=3).fill = openpyxl.styles.PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
                elif qa.confidence == "Low":
                    ws_qa.cell(row=row, column=3).fill = openpyxl.styles.PatternFill(start_color="FFB6C1", end_color="FFB6C1", fill_type="solid")
            
            ws_summary = wb.create_sheet(title="Summary")
            
            total_questions = len(excel_output.questions_answers)
            answered_questions = len([qa for qa in excel_output.questions_answers if qa.is_answered])
            unanswered_questions = total_questions - answered_questions
            
            summary_data = [
                ["Total Questions", total_questions],
                ["Answered Questions", answered_questions],
                ["Unanswered Questions", unanswered_questions],
                ["Answer Rate", f"{(answered_questions/total_questions*100):.1f}%" if total_questions > 0 else "0%"],
                ["", ""],
                ["Confidence Distribution", ""],
                ["High Confidence", len([qa for qa in excel_output.questions_answers if qa.confidence == "High"])],
                ["Medium Confidence", len([qa for qa in excel_output.questions_answers if qa.confidence == "Medium"])],
                ["Low Confidence", len([qa for qa in excel_output.questions_answers if qa.confidence == "Low"])],
                ["Unknown Confidence", len([qa for qa in excel_output.questions_answers if qa.confidence == "Unknown"])],
                ["", ""],
                ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ]
            
            for row, (label, value) in enumerate(summary_data, 1):
                ws_summary.cell(row=row, column=1, value=label)
                ws_summary.cell(row=row, column=2, value=value)
                if label and not str(value).replace(".", "").replace("%", "").isdigit():
                    ws_summary.cell(row=row, column=1).font = openpyxl.styles.Font(bold=True)
            
            if excel_output.unanswered_questions:
                ws_unanswered = wb.create_sheet(title="Unanswered Questions")
                ws_unanswered.cell(row=1, column=1, value="Unanswered Questions")
                ws_unanswered.cell(row=1, column=1).font = openpyxl.styles.Font(bold=True)
                
                for row, question in enumerate(excel_output.unanswered_questions, 2):
                    ws_unanswered.cell(row=row, column=1, value=question)
            
            for ws in wb.worksheets:
                for column in ws.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    ws.column_dimensions[column_letter].width = adjusted_width
            
            wb.save(output_path)
            
        except Exception as e:
            raise Exception(f"Error creating output Excel file: {str(e)}")
    
    @staticmethod
    def validate_excel_file(file_path: str) -> bool:
        """
        Validate if the file is a valid Excel file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if valid Excel file, False otherwise
        """
        try:
            pd.read_excel(file_path, nrows=1)
            return True
        except:
            return False
