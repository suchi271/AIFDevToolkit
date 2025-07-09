from SorthaDevKit.StateBase import FileInputType, FileTypes

Input = {
    "transcript": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\input\sample_transcript.txt",
        type=FileTypes.TEXT
    ),
    "questions_excel": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\input\questions.xlsx",
        type=FileTypes.EXCEL
    ),
    "azure_migrate_report": FileInputType(
        file_path=r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\input\Azure-Migrate-Report.xlsx",
        type=FileTypes.EXCEL
    )
}

# Configuration for output
OUTPUT_CONFIG = {
    "output_file_path": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\filled_aif.xlsx",
    "question_column_name": "Question",  # Name of the column containing questions in Excel
    "excel_sheet_name": None,  # None to use first sheet, or specify sheet name
    # Architecture diagram output configurations
    "architecture_diagram_json": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\architecture_diagram.json",
    "architecture_diagram_svg": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\architecture_diagram.svg",
    "architecture_diagram_xml": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\architecture_diagram.xml",
    "architecture_diagram_vsdx": r"C:\Users\smalisetty\OneDrive - Microsoft\Suchi\MSResearch\DeveloperToolkit\output\architecture_diagram.vsdx"
}
