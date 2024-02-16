from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector

app = Flask(__name__)
CORS(app)  # Active CORS pour tous les domaines

# Clé secrète pour sécuriser l'API
API_KEY = "votre_cle_secrete"

db_config = {
    'host': 'mysql-qcm-service',  # Nom du service Kubernetes
    'port': 3306,  # Port spécifié dans la configuration du service
    'user': 'root',
    'password': '123456',
    'database': 'qcm',
}


conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def validate_api_key(api_key):
    return api_key == API_KEY

#@app.route('/')
#def index():
#   return render_template('ok/login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    if 'api_key' in request.headers and validate_api_key(request.headers['api_key']):
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']
            psswd = generate_password_hash(password, method='pbkdf2:sha256')

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Récupérer le mot de passe haché stocké dans la base de données pour l'utilisateur donné
            cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
            user = cursor.fetchone()

            if user:
                hashed_password_from_db = user[2]  # Assuming the hashed password is stored at index 2 in the database

                # Vérifier si le mot de passe saisi correspond au mot de passe haché dans la base de données
                if (hashed_password_from_db, psswd):
                    user_type = user[3]
                    user_id = user[0]
                    print(user_type)
                    response_data = {'message': 'Authentification réussie', 'user_type': user_type, 'username': username, 'user_id': user_id}
                    return jsonify(response_data)
                else:
                    return jsonify({'message': 'Échec de l\'authentification'}), 401
            else:
                return jsonify({'message': 'Échec de l\'authentification'}), 401
        else:
            return jsonify({'message': 'Données manquantes'}), 400
    else:
        return jsonify({'message': 'Clé API incorrecte'}), 401




@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if 'username' in data and 'password' in data and 'user_type' in data:
        username = data['username']
        password = data['password']
        user_type = data['user_type']

        # Hasher le mot de passe avant de le stocker dans la base de données
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            # Vérifier si le nom d'utilisateur existe déjà
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({'message': 'Le nom d\'utilisateur existe déjà'}), 400

            # Insertion du nouvel utilisateur
            cursor.execute('INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)',
                           (username, hashed_password, user_type))
            conn.commit()

            response_data = {'message': 'Compte créé avec succès', 'user_type': user_type, 'username': username}
            return jsonify(response_data)
        except mysql.connector.Error as err:
            print(f"Erreur MySQL: {err}")
            conn.rollback()
            return jsonify({'message': 'Erreur lors de la création du compte'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Données manquantes'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
