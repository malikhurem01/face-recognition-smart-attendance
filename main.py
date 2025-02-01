from flask import Flask
from flask_cors import CORS
from routes.recognition import recognition_blueprint
from routes.attendance import attendance_blueprint
from routes.venue import venue_blueprint
from database import init_db
from utils.embeddings import generate_face_embeddings

app = Flask(__name__)
CORS(app)

app.register_blueprint(recognition_blueprint)
app.register_blueprint(attendance_blueprint)
app.register_blueprint(venue_blueprint)

if __name__ == '__main__':
    init_db()
    generate_face_embeddings()
    app.run(debug=True)
