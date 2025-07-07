from SorthaDevKit.StateBase import FileInputType, FileTypes

Input = {
    "transcript": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\input\input2.txt",
        type=FileTypes.TEXT
    ),
    "questions_excel": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\input\questions.xlsx",
        type=FileTypes.EXCEL
    )
}

# Configuration for output
OUTPUT_CONFIG = {
    "output_file_path": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\filled_aif.xlsx",
    "question_column_name": "Question",  # Name of the column containing questions in Excel
    "excel_sheet_name": None  # None to use first sheet, or specify sheet name
}
