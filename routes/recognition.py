import os
import numpy as np
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.embeddings import generate_face_embeddings
from utils.face_recognition import face_recognition
from config import KNOWN_FACES_DIR

recognition_blueprint = Blueprint('recognition', __name__)


@recognition_blueprint.route('/recognize_faces', methods=['POST'])
def recognize_faces():
    data = request.get_json()
    image_data = data.get('image')
    if not image_data:
        return jsonify({"error": "Image data is required"}), 400

    recognized_names = face_recognition(image_data)
    return jsonify({'names': recognized_names})


@recognition_blueprint.route('/add_face', methods=['POST'])
def add_face():
    if 'image' not in request.files or 'name' not in request.form:
        return jsonify({"error": "Image and name are required"}), 400

    image = request.files['image']
    name = request.form['name']

    user_folder = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    filename = secure_filename(image.filename)
    image_path = os.path.join(user_folder, filename)
    image.save(image_path)

    generate_face_embeddings()

    return jsonify({"success": True}), 200
