Write-Output 'Establishing virtual environment...'
python -m venv .\venv
Write-Output 'Installing dependencies...'
.\venv\Scripts\pip3.exe install -r .\requirements.txt
Write-Output 'Done!'