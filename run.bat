@echo off

:: Ask the user if they would like to use proxies
echo Would you like to use proxies? (y/n)
choice /c yn /n
if %errorlevel%==1 (
    :: Check if proxies.txt exists
    if exist proxies.txt (
        :: Read the HTTP and HTTPS proxies from proxies.txt
        set /p http_proxy=<proxies.txt
        <proxies.txt (
            set /p=
            set /p https_proxy=
        )
        echo HTTP proxy settings have been applied: %http_proxy%
        echo HTTPS proxy settings have been applied: %https_proxy%
    ) else (
        echo proxies.txt not found. No proxy settings applied.
    )
) else (
    echo No proxy settings applied.
)

:: Check if Python is installed by trying to display its version
echo Checking for Python installation...
python -V >nul 2>&1 || (
    :: If Python is not installed, open the Python download page in the user's default web browser
    echo Python is not installed. Attempting to open the Python download page.
    start "https://www.python.org/downloads/"
    :: Pause to keep the console window open, then exit the batch file
    pause
    exit /b
)
echo Python installation found.

:: Check if pip is installed by trying to display its version
echo Checking for pip installation...
python -m pip -V >nul 2>&1 || (
    :: If pip is not installed, inform the user and exit the batch file
    echo pip is not installed. Please ensure Python is correctly installed and try again.
    pause
    exit /b
)
echo pip installation found.

:: Change the working directory to the location of the batch file
cd /D %~dp0

:: Move to 'code' directory
cd code

:: Use pip to install the Python packages specified in requirements.txt located in root directory
echo Checking if requirements.txt modules are up to date...
python -m pip install -r ..\requirements.txt > temp.txt

:: Check if the temporary file contains the word "Installing" or "Upgrading"
findstr /C:"Installing" /C:"Upgrading" temp.txt >nul 2>&1
if !errorlevel! == 0 (
    echo Updates found:
    type temp.txt
) else (
    echo Requirements are up to date.
)
:: Delete the temporary file
del temp.txt

:: Download NLTK corpora 'stopwords' and 'wordnet'
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

:: Use Streamlit to run the application script in the background
start /B streamlit run Streamlit\app.py

:: Provide an option to kill the Streamlit app
:menu
echo Press 'k' to kill the Streamlit app or 'q' to quit the command prompt.
choice /c kq /n
if %errorlevel%==1 (
    :: Kill the Streamlit app
    taskkill /IM streamlit.exe /F
    cd .. 
    goto normal_prompt
)
if %errorlevel%==2 (
    :: Kill command prompt
    exit /b
)

:normal_prompt
cmd /k