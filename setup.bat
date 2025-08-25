@echo off
echo ================================================
echo   Azure Migration Assessment Tool Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

echo.
echo Setting up virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take a few minutes...

REM Install core dependencies
pip install --upgrade pip
pip install python-docx openpyxl pandas
pip install openai python-dotenv
pip install langchain-openai
pip install typing-extensions

if %errorlevel% neq 0 (
    echo ERROR: Failed to install some packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Creating .env file template...
if not exist .env (
    echo # Azure Migration Assessment Tool Configuration > .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo # Get your API key from https://platform.openai.com/api-keys >> .env
    echo. >> .env
    echo # Optional: Azure OpenAI Configuration >> .env
    echo # AZURE_OPENAI_API_KEY=your_azure_openai_key >> .env
    echo # AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/ >> .env
    echo # AZURE_OPENAI_API_VERSION=2024-02-15-preview >> .env
    echo.
    echo .env file created. Please edit it with your API keys.
) else (
    echo .env file already exists.
)

echo.
echo Creating input and output directories...
if not exist input mkdir input
if not exist output mkdir output

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit the .env file and add your OpenAI API key
echo 2. Place your input files in the 'input' directory:
echo    - Transcript file (sample_transcript.txt)
echo    - Azure Migrate report (Azure-Migrate-Report.xlsx)
echo    - Questions file (questions_new.xlsx)
echo    - Dependency analysis (optional)
echo 3. Run the tool with: python main.py
echo.
echo To activate the environment later, run: venv\Scripts\activate.bat
echo.
pause
