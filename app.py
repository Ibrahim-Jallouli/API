from flask import Flask
from routes import routes

app = Flask(__name__)

# Enregistrer les routes depuis le fichier routes.py
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(debug=True)
