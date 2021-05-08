echo 'Establishing virtual environment...'
python3 -m venv ./lvenv
echo 'Installing dependencies...'
./lvenv/bin/pip3 install -r ./requirements.txt
echo 'Done'