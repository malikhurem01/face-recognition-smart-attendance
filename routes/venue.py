from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from database import venues_collection

venue_blueprint = Blueprint('venue', __name__)

@venue_blueprint.route('/get-all-venues', methods=['GET'])
def get_all_venues():
    try:
        venues = venues_collection.find()
        venues_list = []
        for venue in venues:
            venue_data = {
                "_id": str(venue["_id"]),
                "name": venue["name"],
                "date_time": venue["date_time"].strftime("%Y-%m-%d %H:%M:%S"),
                "attendance": venue.get("attendance", [])
            }
            venues_list.append(venue_data)
        return jsonify({"venues": venues_list}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching venues: {str(e)}"}), 500

@venue_blueprint.route('/create-attendance-venue', methods=['POST'])
def create_attendance_venue():
    data = request.get_json()
    venue_name = data.get('name')
    venue_date_time = data.get('date_time')

    if not venue_name or not venue_date_time:
        return jsonify({"error": "Name and date_time are required"}), 400

    # If the incoming date_time is missing seconds, append them.
    if len(venue_date_time) == 16:
        venue_date_time += ":00"

    try:
        venue_date_time = datetime.strptime(venue_date_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid date_time format. Expected format: YYYY-MM-DD HH:MM:SS"}), 400

    venue_data = {
        "name": venue_name,
        "date_time": venue_date_time,
        "attendance": []
    }

    try:
        result = venues_collection.insert_one(venue_data)
        venue_data["_id"] = str(result.inserted_id)
    except Exception as e:
        return jsonify({"error": f"Could not insert venue data. Error: {str(e)}"}), 400

    return jsonify({"message": "Venue created successfully!", "venue_id": venue_data["_id"]}), 201
