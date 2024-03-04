import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Ajouter le répertoire parent au chemin

from app import app


class TestDownload(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_download(self):
        # Envoi d'une requête GET à la route /download_image
        response = self.app.get('/download_image')

        # Vérification du code de statut de la réponse
        self.assertEqual(response.status_code, 200)

        # Vérification du type MIME de la réponse
        self.assertEqual(response.mimetype, 'image/png')

        # Vérification du téléchargement en tant que pièce jointe
        self.assertTrue('attachment' in response.headers['Content-Disposition'])

if __name__ == '__main__':
    unittest.main()
