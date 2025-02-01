import os
import pickle
from deepface import DeepFace
from config import VECTOR_DB_DIR, KNOWN_FACES_DIR

if not os.path.exists(VECTOR_DB_DIR):
    os.makedirs(VECTOR_DB_DIR)

def load_embeddings():
    embeddings_path = os.path.join(VECTOR_DB_DIR, 'face_embeddings.pkl')
    if os.path.exists(embeddings_path):
        with open(embeddings_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def save_embeddings(embeddings):
    with open(os.path.join(VECTOR_DB_DIR, 'face_embeddings.pkl'), 'wb') as f:
        pickle.dump(embeddings, f)

def generate_face_embeddings():
    embeddings_dict = {}
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_folder = os.path.join(KNOWN_FACES_DIR, person_name)
        if os.path.isdir(person_folder):
            embeddings_dict[person_name] = []
            for img_file in os.listdir(person_folder):
                img_path = os.path.join(person_folder, img_file)
                embedding = DeepFace.represent(img_path, model_name="VGG-Face", enforce_detection=False)
                embeddings_dict[person_name].append(embedding[0]["embedding"])
    save_embeddings(embeddings_dict)

def generate_one_face_embedding(image_path, name):
    embedding = DeepFace.represent(image_path, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
    stored_embeddings = load_embeddings()
    if name in stored_embeddings:
        stored_embeddings[name].append(embedding)
    else:
        stored_embeddings[name] = [embedding]
    save_embeddings(stored_embeddings)
    return embedding
