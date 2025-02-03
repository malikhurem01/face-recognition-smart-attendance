# Smart Attendance System

A face recognition-based attendance tracking system built with Python, Flask, DeepFace, OpenCV and MongoDB.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project is a face recognition attendance system. It detects and recognizes faces in an image to update attendance records for different venues. The system leverages:

- **Flask** for creating RESTful API endpoints.
- **DeepFace** and **OpenCV** for face detection and recognition.
- Local **Vector** database to securely store face embedings.
- **MongoDB** for storing attendance venue data.
- **Pickle** for saving and loading face embeddings.

## Features

- **Face Recognition:** Recognize faces from a base64-encoded image.
- **Attendance Management:** Create venues and update attendance records automatically.
- **Add Faces:** Upload new images to add faces to the known faces database.
- **Data Persistence:** Store venue and attendance data using MongoDB.
- **Cross-Origin Resource Sharing (CORS):** Allows the API to be accessed from different domains.

## Requirements

- Python 3.12+
- MongoDB (Atlas or a local installation)

### Python Packages

- flask
- flask\_cors
- pymongo
- opencv-python
- deepface
- numpy
- pillow
- bson
- werkzeug

You can install the required packages using pip (see [Installation](#installation)).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/malikhurem01/face-recognition-smart-attendance.git
   cd face-recognition-smart-attendance
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

3. **Install the dependencies:**

   If you have a `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install packages individually:

   ```bash
   pip install flask flask_cors pymongo opencv-python deepface numpy pillow bson werkzeug
   ```

4. **Configure MongoDB Connection:**

   The MongoDB connection string is currently hard-coded in the code. For production use, consider moving this configuration to environment variables or a separate configuration file.

## Project Structure

```
.
├── app.py                  # Main Flask application with all endpoints
├── README.md               # Project documentation
├── requirements.txt        # List of Python dependencies
└── database
    ├── users               # Directory to store images of known faces
    └── vectors             # Directory to store face embeddings (pickle file)
```

## Usage

### Running the Application

To start the Flask server, run:

```bash
python main.py
```

By default, the application runs in debug mode on [http://127.0.0.1:5000](http://127.0.0.1:5000). **Note:** Disable debug mode in production.

### API Endpoints

#### 1. `/recognize_faces` (POST)

- **Description:**\
  Recognize faces from a base64-encoded image.

- **Request Payload:**

  ```json
  {
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
  }
  ```

- **Response Example:**

  ```json
  {
    "names": ["JohnDoe", "JaneDoe"]
  }
  ```

#### 2. `/get-attendance` (POST)

- **Description:**\
  Recognize faces in an image for a specific attendance venue and update the attendance records.

- **Request Payload:**

  ```json
  {
    "venue_id": "609e1250f1a4a3d3b8f9d0f1",  
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
  }
  ```

- **Response Example:**

  ```json
  {
    "message": "Attendance updated successfully",
    "venue_id": "609e1250f1a4a3d3b8f9d0f1",
    "attendance": ["JohnDoe"],
    "recognized_names": ["JohnDoe"]
  }
  ```

#### 3. `/add_face` (POST)

- **Description:**\
  Add a new face image to the known faces database.

- **Request Payload:**\
  This endpoint expects form-data with the following keys:

  - `image`: The image file.
  - `name`: The name associated with the face.

- **Response Example:**

  ```json
  {
    "success": true
  }
  ```

## Notes

- **Face Embeddings:**\
  Embeddings are generated for every image in the `database/users` directory and saved as a pickle file in `database/vectors`. When adding a new face, the application regenerates all embeddings, which might be inefficient as the dataset grows. Consider optimizing this for larger deployments.

- **Security Considerations:**

  - Validate and sanitize all inputs.
  - Disable debug mode in production.
  - Modify the generate_all_embeddings method to delete photos from database/users directory after securely embedding them in the .pkl file.

- **Error Handling:**\
  Basic error handling is implemented. You might need to extend this to cover more edge cases and improve the robustness of the application.

## Contributing

Contributions are welcome! If you have any suggestions, bug fixes, or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [DeepFace](https://github.com/serengil/deepface) for providing face recognition capabilities.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [OpenCV](https://opencv.org/) for computer vision and image processing.

