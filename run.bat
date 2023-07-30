@echo off

:: Check if Python is installed by trying to display its version
python -V >nul 2>&1 || (
    :: If Python is not installed, open the Python download page in the user's default web browser
    echo Python is not installed. Attempting to open the Python download page.
    start "https://www.python.org/downloads/"
    :: Pause to keep the console window open, then exit the batch file
    pause
    exit /b
)

:: Check if pip is installed by trying to display its version
python -m pip -V >nul 2>&1 || (
    :: If pip is not installed, inform the user and exit the batch file
    echo pip is not installed. Please ensure Python is correctly installed and try again.
    pause
    exit /b
)

:: Change the working directory to the location of the batch file
cd /D %~dp0

:: Move to 'code' directory
cd code

:: Use pip to install the Python packages specified in requirements.txt located in root directory
python -m pip install -r ..\requirements.txt

:: Use Streamlit to run the application script
streamlit run Streamlit\app.py

:: Pause to keep the console window open after the Streamlit command
pause