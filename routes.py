from functools import wraps
from flask import Blueprint, render_template, request, send_file, jsonify
from PIL import Image, ImageOps
import io
import base64
import mysql.connector

db_config = {
    'user': 'root',
    'password':'',
    'host': '127.0.0.1',
    'database': 'api_transformation_image',
}

routes = Blueprint('routes', __name__)

def verifier_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        print(api_key)
        
        # Vérifier si l'API key est présente dans la base de données
        try:
            conn = mysql.connector.connect(**db_config)
            print(conn)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE apikey = %s", (api_key,))
            utilisateur_id = cursor.fetchone()

            if utilisateur_id:
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'API key invalide'}), 401

        except mysql.connector.Error as err:
            return jsonify({'message': 'Erreur de base de données'}), 500

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()

    return wrapper


@routes.route('/')
#@verifier_api_key
def index():
    return render_template('index.html')

@routes.route('/upload', methods=['POST'])
#@verifier_api_key
def upload():
    # Récupération du fichier
    file = request.files['file']

    # Ouverture de l'image d'origine
    original_image = Image.open(file)

    # Enregistrement de l'image d'origine en mémoire
    img_byte_array = io.BytesIO()
    original_image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return send_file(img_byte_array, mimetype='image/png', as_attachment=True, download_name='original_image.png')

@routes.route('/invert_horizontal', methods=['POST'])
#@verifier_api_key
def invert_horizontal():
    return apply_transformation(ImageOps.mirror)

@routes.route('/invert_vertical', methods=['POST'])
#@verifier_api_key
def invert_vertical():
    return apply_transformation(ImageOps.flip)

@routes.route('/invert_colors', methods=['POST'])
#@verifier_api_key
def invert_colors():
    return apply_transformation(lambda img: ImageOps.invert(img.convert('RGB')))

@routes.route('/rotate', methods=['POST'])
#@verifier_api_key
def rotate():
    return apply_transformation(lambda img: img.rotate(90))

@routes.route('/change_color', methods=['POST'])
#@verifier_api_key
def change_color():
    return apply_transformation(lambda img: img.convert('L'))

def apply_transformation(transformation_func):
    # Récupération des données JSON
    data = request.get_json()
    image_data = data['image_data'].split(',')[1]  # Ignorez le préfixe 'data:image/png;base64,'

    # Décoder l'image à partir des données base64
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    # Appliquer la transformation
    image = transformation_func(image)

    # Enregistrer l'image transformée en mémoire
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    modified_path="./modified_image.png"
    image.save(modified_path)
    img_byte_array.seek(0)

    # Retourner l'image transformée en tant que réponse JSON
    return jsonify({'image_url': f'data:image/png;base64,{base64.b64encode(img_byte_array.read()).decode()}'})

@routes.route('/download_image', methods=['GET'])
#@verifier_api_key
def download_image():
    return send_file('./modified_image.png', mimetype='image/png', as_attachment=True, download_name='modified_image.png')
