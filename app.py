from flask import Flask, Response, jsonify
import os
import time
from pathlib import Path

app = Flask(__name__)

basedir = Path(__file__).parent

# Directory where cheat sheet files are stored
CHEAT_SHEETS_DIR = 'cheat_sheets'

# Function to load cheat sheet from a text file
def load_cheat_sheet(command):
    file_path = basedir / f"{CHEAT_SHEETS_DIR}/{command}"
    if os.path.exists(file_path):
        print(file_path)
        with open(file_path, 'r') as file:
            return file.read()
    return None

@app.route('/healthz')
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.route('/<command>', methods=['GET'])
def get_cheat_sheet(command):
    command = command.lower()  # Normalize the command to lowercase
    cheat_sheet = load_cheat_sheet(command)

    if cheat_sheet:
        return Response(cheat_sheet, mimetype='text/plain')
    else:
        return Response("Cheat sheet not found for the specified command.", status=404)


@app.route('/commands', methods=['GET'])
def list_commands():
    # Get the list of all text files in the cheat_sheets directory
    directory = basedir / CHEAT_SHEETS_DIR
    commands = [filename for filename in os.listdir(directory)]
    return jsonify(commands), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
