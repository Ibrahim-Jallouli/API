import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Ajouter le répertoire parent au chemin

from app import app

from app import app
from io import BytesIO
from PIL import Image

class TestUpload(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_upload(self):
        # Création d'un objet de fichier simulé avec le contenu de l'image réelle
        file_path = './resources/test_image.png'
        with open(file_path, 'rb') as file:
            file_contents = file.read()
            file = BytesIO(file_contents)
            file.name = 'test_image.png'

            # Envoi d'une requête POST à la route /upload avec le fichier simulé
            response = self.app.post('/upload', data={'file': file})

            # Vérification du code de statut de la réponse
            self.assertEqual(response.status_code, 200)

            # Vérification du type MIME de la réponse
            self.assertEqual(response.mimetype, 'image/png')

            # Ouvrir l'image renvoyée par l'application Flask avec Pillow
            uploaded_image = Image.open(BytesIO(response.data))

            # Ouvrir l'image simulée avec Pillow
            simulated_image = Image.open(file_path)

            # Comparer les données d'image brutes
            self.assertEqual(uploaded_image.tobytes(), simulated_image.tobytes())

if __name__ == '__main__':
    unittest.main()
