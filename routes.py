from flask import Blueprint, render_template, request, send_file, jsonify
from PIL import Image, ImageOps
import io
import base64

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/upload', methods=['POST'])
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
def invert_horizontal():
    return apply_transformation(ImageOps.mirror)

@routes.route('/invert_vertical', methods=['POST'])
def invert_vertical():
    return apply_transformation(ImageOps.flip)

@routes.route('/invert_colors', methods=['POST'])
def invert_colors():
    return apply_transformation(lambda img: ImageOps.invert(img.convert('RGB')))

@routes.route('/rotate', methods=['POST'])
def rotate():
    return apply_transformation(lambda img: img.rotate(90))

@routes.route('/change_color', methods=['POST'])
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
def download_image():
    return send_file('./modified_image.png', mimetype='image/png', as_attachment=True, download_name='modified_image.png')
