from flask import Flask, render_template, request, jsonify
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'audio_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    # Ignore temporary scrub files created by SoX
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.wav') and not f.startswith('temp_')]
    return jsonify(files)

@app.route('/file_info', methods=['POST'])
def file_info():
    filename = request.form.get('audio_file')
    if not filename: 
        return jsonify({"duration": 0})
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        # Use SoX to calculate exact audio duration, bypassing Python's wave module errors
        result = subprocess.run(["soxi", "-D", filepath], capture_output=True, text=True)
        duration = float(result.stdout.strip())
        return jsonify({"duration": duration})
    except:
        return jsonify({"duration": 0})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file detected"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if file and file.filename.endswith('.wav'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"success": "File uploaded", "filename": filename})
        
    return jsonify({"error": "Invalid file. Only .wav is supported."}), 400

@app.route('/broadcast', methods=['POST'])
def broadcast():
    # Kill any existing radio, mic, or audio streams
    subprocess.run(["sudo", "pkill", "pi_fm_rds"])
    subprocess.run(["sudo", "pkill", "sox"])
    subprocess.run(["sudo", "pkill", "arecord"]) 
    
    freq = request.form.get('freq', '107.9')
    filename = request.form.get('audio_file')
    offset = float(request.form.get('offset', 0))
    
    if not filename:
        return jsonify({"error": "No file selected"}), 400
        
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
        
    # THE FIX: Pipe SoX output directly into the transmitter's stdin (-)
    # This prevents infinite looping and handles exact timestamp trimming flawlessly.
    cmd = f"sox \"{filepath}\" -t wav - trim {offset} | sudo ./pi_fm_rds -audio - -freq {freq}"
    subprocess.Popen(cmd, shell=True)
    
    return jsonify({"success": "Transmitting"})

@app.route('/mic', methods=['POST'])
def mic_broadcast():
    # Free the transmitter and microphone hardware
    subprocess.run(["sudo", "pkill", "pi_fm_rds"])
    subprocess.run(["sudo", "pkill", "arecord"])
    
    freq = request.form.get('freq', '107.9')
    
    # Capture live USB mic audio and pipe it to the transmitter
    cmd = f"arecord -D plughw:2,0 -f S16_LE -r 44100 -c 2 -t wav | sudo ./pi_fm_rds -audio - -freq {freq}"
    subprocess.Popen(cmd, shell=True)
    
    return jsonify({"success": "Live Mic Active"})

@app.route('/stop', methods=['POST'])
def stop():
    # Ensure all processes are terminated
    subprocess.run(["sudo", "pkill", "pi_fm_rds"])
    subprocess.run(["sudo", "pkill", "arecord"])
    subprocess.run(["sudo", "pkill", "sox"])
    return jsonify({"success": "Halted"})

# --- Telemetry Engine ---
@app.route('/stats', methods=['GET'])
def stats():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = round(float(f.read()) / 1000.0, 1)
    except:
        temp = 0.0

    try:
        load = round(os.getloadavg()[0], 2)
    except:
        load = 0.0

    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            total = int(lines[0].split()[1])
            free = int(lines[1].split()[1])
            buffers = int(lines[3].split()[1])
            cached = int(lines[4].split()[1])
            used = total - free - buffers - cached
            mem_percent = round((used / total) * 100, 1)
    except:
        mem_percent = 0.0

    rx_bytes, tx_bytes = 0, 0
    try:
        with open('/proc/net/dev', 'r') as f:
            for line in f.readlines():
                if 'wlan0:' in line or 'eth0:' in line:
                    parts = line.split(':')
                    data = parts[1].split()
                    rx_bytes += int(data[0])
                    tx_bytes += int(data[8])
    except:
        pass

    return jsonify({
        "temp": temp, "load": load, "mem": mem_percent, "rx": rx_bytes, "tx": tx_bytes
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767)
