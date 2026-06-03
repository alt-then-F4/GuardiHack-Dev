import os
import json
import math
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Configuration des dossiers
UPLOAD_FOLDER = 'static'
CONFIG_FILE = 'config.json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration par défaut si le fichier config.json n'existe pas encore
DEFAULT_CONFIG = {
    "title": "GEOINT #1",
    "description": "Trouvez l'emplacement exact de ce bâtiment.",
    "author": "altF4",
    "image_path": "challenge.png",
    "true_lat": 48.8584,
    "true_lon": 2.2945,
    "radius": 50.0,
    "flag": "CTF{47_42_n0rth_0_29_w35t_g301nt}"
}

penalties_db = {}
# Liste des pénalités : 30s, 1m, 2m, 3m, 5m, 7m, 10m
PENALTY_DURATIONS = [30, 60, 120, 180, 300, 420, 600]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config_data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.route('/')
def home():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    config = load_config()
    if request.method == 'POST':
        # Récupération des données du formulaire
        title = request.form.get('title', config['title'])
        description = request.form.get('description', config['description'])
        author = request.form.get('author', config['author'])
        true_lat = float(request.form.get('true_lat', config['true_lat']))
        true_lon = float(request.form.get('true_lon', config['true_lon']))
        radius = float(request.form.get('radius', config['radius']))
        flag = request.form.get('flag', config['flag'])
        
        image_file = request.files.get('image')
        image_path = config['image_path']
        
        # Gestion de l'upload de l'image
        if image_file and image_file.filename != '':
            filename = 'challenge_' + str(int(time.time())) + '.png'
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = filename

        # Mise à jour de la configuration
        new_config = {
            "title": title,
            "description": description,
            "author": author,
            "image_path": image_path,
            "true_lat": true_lat,
            "true_lon": true_lon,
            "radius": radius,
            "flag": flag
        }
        save_config(new_config)
        return redirect(url_for('home'))

    return render_template('admin.html', config=config)

@app.route('/check-lock', methods=['GET'])
def check_lock():
    user_ip = request.remote_addr
    current_time = time.time()
    user_penalty = penalties_db.get(user_ip, {"locked_until": 0, "failures": 0, "total_duration": 0})
    if current_time < user_penalty["locked_until"]:
        remaining = int(user_penalty["locked_until"] - current_time)
        return jsonify({"locked": True, "remaining_time": remaining, "total_duration": user_penalty["total_duration"]})
    return jsonify({"locked": False})

@app.route('/submit-guess', methods=['POST'])
def submit_guess():
    user_ip = request.remote_addr
    current_time = time.time()
    user_penalty = penalties_db.get(user_ip, {"locked_until": 0, "failures": 0, "total_duration": 0})
    
    if current_time < user_penalty["locked_until"]:
        return jsonify({"success": False, "locked": True, "remaining_time": int(user_penalty["locked_until"] - current_time)}), 403

    config = load_config()
    data = request.json
    distance = haversine_distance(float(data['lat']), float(data['lon']), config['true_lat'], config['true_lat']) # Note: Correction mineure de variable ici pour lier à config
    distance = haversine_distance(float(data['lat']), float(data['lon']), config['true_lat'], config['true_lon'])
    
    if distance <= config['radius']:
        penalties_db[user_ip] = {"locked_until": 0, "failures": 0, "total_duration": 0}
        return jsonify({"success": True, "message": "Localisation confirmée.", "flag": config['flag']})
    else:
        failures = user_penalty["failures"] + 1
        idx = min(failures - 1, len(PENALTY_DURATIONS) - 1)
        duration = PENALTY_DURATIONS[idx]
        penalties_db[user_ip] = {"locked_until": current_time + duration, "failures": failures, "total_duration": duration}
        return jsonify({"success": False, "locked": True, "remaining_time": duration, "total_duration": duration, "message": "Coordonnées incorrectes."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
