@echo off
setlocal

REM --- Command Definitions ---
if /I "%1" == "help" goto :help
if /I "%1" == "setup" goto :setup
if /I "%1" == "install" goto :install
if /I "%1" == "setup-env" goto :setup_env
if /I "%1" == "run-weather-server" goto :run_weather_server
if /I "%1" == "run-weather-client" goto :run_weather_client
if /I "%1" == "run-remote-server" goto :run_remote_server
if /I "%1" == "run-remote-client" goto :run_remote_client

echo Invalid command: %1
goto :help

:help
echo.
echo Available commands for Windows (run.bat):
echo   setup              - Create a Python virtual environment and install dependencies
echo   install            - Install Python dependencies (for manual venv management)
echo   setup-env          - Guide to create .env file from .env.example
echo   run-weather-server - Run the standalone weather tool server
echo   run-weather-client - Run the GenAI agent client for the weather server
echo   run-remote-server  - Run the authenticated FastAPI server
echo   run-remote-client  - Run the client for the authenticated server (requires MCP_CLIENT_TOKEN)
echo.
goto :eof

:setup
if not exist venv\ (
    echo Creating Python virtual environment in 'venv'...
    python -m venv venv
) else (
    echo Virtual environment 'venv' already exists.
)
echo Installing dependencies...
call venv\Scripts\pip.exe install -r requirements.txt
echo.
echo Setup complete. Activate the virtual environment with: venv\Scripts\activate.bat
goto :eof

:install
echo Installing dependencies...
pip install -r requirements.txt
goto :eof

:setup_env
echo Please copy the '.env.example' file to a new file named '.env'.
echo Then, open '.env' and add your GENAI_API_KEY.
echo You can use the command: copy .env.example .env
goto :eof

:run_weather_server
python example/server/weather.py
goto :eof

:run_weather_client
python example/client/client.py
goto :eof

:run_remote_server
python main_remote.py
goto :eof

:run_remote_client
python client_remote.py
goto :eof

:eof
endlocal