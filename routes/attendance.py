import numpy as np
from flask import Blueprint, request, jsonify
from utils.face_recognition import face_recognition
from bson import ObjectId
from database import venues_collection

attendance_blueprint = Blueprint('attendance', __name__)


@attendance_blueprint.route('/get-attendance', methods=['POST'])
def get_attendance():
    data = request.get_json()
    venue_id = data.get('venue_id')
    image_data = data.get('image')

    if not venue_id or not image_data:
        return jsonify({"error": "venue_id and image are required"}), 400

    try:
        venue_id_obj = ObjectId(venue_id)
    except Exception:
        return jsonify({"error": "Invalid venue_id format"}), 400

    venue = venues_collection.find_one({"_id": venue_id_obj})
    if not venue:
        return jsonify({"error": "Venue not found"}), 404

    recognized_names = face_recognition(image_data)
    existing_attendance = venue.get("attendance", [])
    new_names = [name for name in recognized_names if name not in existing_attendance]

    if new_names:
        venues_collection.update_one(
            {"_id": venue_id_obj},
            {"$addToSet": {"attendance": {"$each": new_names}}}
        )

    updated_venue = venues_collection.find_one({"_id": venue_id_obj}, {"_id": 1, "attendance": 1})
    return jsonify({
        "message": "Attendance updated successfully",
        "venue_id": str(venue_id),
        "attendance": updated_venue.get("attendance", []),
        "recognized_names": recognized_names
    }), 200
