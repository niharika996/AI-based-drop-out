# Backend Service for SIH Project

## Overview
This backend service is a Flask-based API server that manages students, mentors, subjects, and predictions data. It connects to a MongoDB database to store and retrieve information.

## Requirements
- Python 3.7 or higher
- MongoDB instance running locally or remotely
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository or download the project files.

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory (if not present).
   - Add the MongoDB connection string:
     ```
     MONGO_URI=mongodb://localhost:27017/
     ```
   - Adjust the URI if your MongoDB instance is hosted elsewhere.

## Running the Backend

Run the Flask application using the following command:
```bash
python backend/app.py
```

The server will start on `http://localhost:5000` with debug mode enabled.

## API Endpoints

The backend exposes the following main API endpoints:

- `/api/students` - Manage student data (GET, POST)
- `/api/mentors` - Manage mentor data (GET, POST)
- `/api/subjects` - Manage subject data (GET, POST)
- `/api/predictions` - Manage prediction data (GET, POST)

## Notes

- Ensure MongoDB is running and accessible before starting the backend.
- The backend uses Flask Blueprints to organize routes.
- Debug mode is enabled by default for development purposes.

## Troubleshooting

- If you encounter database connection errors, verify your `MONGO_URI` and MongoDB server status.
- For any missing dependencies, re-run the installation command.

## License

This project is licensed under the MIT License.
