from SorthaDevKit.StateBase import FileInputType, FileTypes

Input = {
    "transcript": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Desktop\DeveloperToolkit\input\sample_transcript.txt",
        type=FileTypes.TEXT
    ),
    "questions_excel": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Desktop\DeveloperToolkit\input\input_aif.xlsx",
        type=FileTypes.EXCEL
    )
}

# Configuration for output
OUTPUT_CONFIG = {
    "output_file_path": r"C:\Users\smalisetty\OneDrive - Microsoft\Desktop\DeveloperToolkit\output\filled_aif.xlsx",
    "question_column_name": "Question",
    "excel_sheet_name": None
}
