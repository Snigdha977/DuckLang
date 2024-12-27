#!/bin/bash

detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "MacOS";;
        CYGWIN*|MINGW*|MSYS*) echo "Windows";;
        *)          echo "Unknown";;
    esac
}


echo "Welcome to the DuckLang Setup Script!"


OS=$(detect_os)
echo "Detected OS: $OS"


if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and rerun the script."
    exit 1
fi


echo "Creating virtual environment..."
python3 -m venv venv


echo "Activating virtual environment..."
source venv/bin/activate


read -p "Do you want to create a .env file? (y/n): " CREATE_ENV
if [[ "$CREATE_ENV" == "y" || "$CREATE_ENV" == "Y" ]]; then
    echo "Creating .env file..."
    touch .env
    echo "Add your configuration variables to .env (e.g., DUCKLANG_DEBUG=True)"
fi


echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Skipping dependency installation."
fi


echo "Starting the DuckLang interpreter..."
python3 main.py


deactivate
