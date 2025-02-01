import numpy as np
from deepface import DeepFace
from utils.embeddings import load_embeddings
from utils.image_processing import decode_image, detect_faces


def face_recognition(image_data):
    img_array = decode_image(image_data)
    faces = detect_faces(img_array)
    recognized_names = []
    stored_embeddings = load_embeddings()

    for (x, y, w, h) in faces:
        face_crop = img_array[y:y + h, x:x + w]
        face_embedding = DeepFace.represent(face_crop, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
        best_match_name = None
        best_match_distance = float('inf')

        for person_name, embeddings in stored_embeddings.items():
            for embedding in embeddings:
                distance = np.linalg.norm(face_embedding - np.array(embedding))
                if distance < best_match_distance:
                    best_match_distance = distance
                    best_match_name = person_name

        recognized_names.append(best_match_name if best_match_name else 'Unknown')

    recognized_names = list(set(recognized_names))
    return recognized_names
