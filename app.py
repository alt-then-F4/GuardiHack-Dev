from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/victoire', methods=['POST'])
def check_win():
    data = request.get_json()
    
    # Le serveur vérifie que le joueur a 7 points ET que la preuve mathématique vaut 1415
    if data and data.get('score_p') == 7 and data.get('proof') == 1415:
        return jsonify({
            "status": "success",
            "flag": "CTF{Byp4ss_L0c4l_Sc0p3_W1th_Br34kp01nt}"
        })
    
    return jsonify({"status": "error", "message": "Preuve de jeu invalide ou score incorrect."}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
