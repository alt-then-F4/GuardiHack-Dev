🏗️ Structure du Projet
Avant de commencer, assure-toi que tes fichiers sont organisés comme suit dans ton dossier ~/PuckOverride :

app.py (Serveur Flask)

Dockerfile (Configuration de l'image)

requirements.txt (Dépendances Python)

templates/

index.html (Le jeu avec les sécurités appliquées)

🛠️ Étape 1 : Configuration du Serveur (app.py)
Ce fichier gère la validation des scores et de la preuve mathématique générée par le jeu.

Python
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/victoire', methods=['POST'])
def check_win():
    data = request.get_json()
    
    # Validation du score (7) et de la preuve mathématique (1415)
    if data and data.get('score_p') == 7 and data.get('proof') == 1415:
        return jsonify({
            "status": "success",
            "flag": "CTF{Byp4ss_L0c4l_Sc0p3_W1th_Br34kp01nt}"
        })
    
    return jsonify({"status": "error", "message": "Requête invalide."}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
🎨 Étape 2 : Configuration du Jeu (index.html)
Assure-toi que ton fichier index.html contient bien les éléments de sécurité et de design demandés :

Variables camouflées : _renderRefreshRateDelta = 15.0 (vitesse de l'IA).

Preuve Bitwise : proof = (((proof << 3) - proof) + 0x539) % 0x186a0;.

API Masquée : atob("L2FwaS92aWN0b2lyZQ==").

Design : Titre "PuckOverride", auteur "altF4", et mention du design par Matt Cannon.

🐳 Étape 3 : Déploiement avec Docker
C'est la méthode la plus propre pour isoler le challenge sur ta VM Ubuntu.

Créer le fichier requirements.txt :

flask


2.  **Créer le `Dockerfile`** :
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    RUN pip install --no-cache-dir -r requirements.txt
    EXPOSE 80
    CMD ["python", "app.py"]
Lancer le build et l'exécution :

Bash
sudo docker build -t puck-override .
sudo docker run -d -p 80:80 --name puck-challenge puck-override

---

## 🧪 Étape 4 : Vérification du Challenge
Une fois le conteneur lancé, effectue ces tests pour t'assurer que tout fonctionne :
1.  **Accès** : Va sur `http://TON_IP_VM`. Tu dois voir l'interface "PuckOverride".
2.  **Sécurité** : Ouvre la console et tape `_renderRefreshRateDelta`. Tu dois obtenir une erreur `ReferenceError`.
3.  **Résolution** : 
    *   Va dans l'onglet **Sources** de l'inspecteur.
    *   Pose un breakpoint dans la fonction `updateCPU`.
    *   Dans **Scope > Closure**, change `_renderRefreshRateDelta` à `1.0`.
    *   Gagne 7-0 et vérifie que le Flag s'affiche bien après l'analyse.

---

## 🚀 Étape 5 : Mise à jour sur GitHub
Maintenant que ta configuration est propre, n'oublie pas de synchroniser ton dépôt pour garder une trace de ton travail :
```bash
git add .
git commit -m "Mise à jour finale : Sécurités, Camouflage et Design"
git push origin main
