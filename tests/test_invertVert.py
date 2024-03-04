import unittest
import os
import sys
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from app import app

class TestInvertHorizontal(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_invert_horizontal(self):
        # Load a sample image for testing (you may want to replace this with a real image path)
        sample_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './resources/test_image.png'))

        # Open the sample image and encode it in base64
        with open(sample_image_path, 'rb') as f:
            sample_image_content = f.read()

        sample_image_base64 = base64.b64encode(sample_image_content).decode('utf-8')

        # Send a POST request to the /invert_horizontal route with the sample image
        response = self.app.post('/invert_vertical', json={'image_data': f'data:image/png;base64,{sample_image_base64}'})

        # Check the status code of the response
        self.assertEqual(response.status_code, 200)

        # Check the MIME type of the response
        self.assertEqual(response.mimetype, 'application/json')

        # Check if the 'image_url' key is present in the response JSON
        self.assertIn('image_url', response.json)


if __name__ == '__main__':
    unittest.main()
