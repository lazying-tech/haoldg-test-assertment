### Setup Instructions

Follow the steps below to set up and run the project:

## 1. Create a Virtual Environment

# On Windows:

python -m venv venv

# On MacOS/Linux:

python3 -m venv venv

## 2. Activate the Virtual Environment

# On Windows:

venv\Scripts\activate

# On MacOS/Linux:

source venv/bin/activate

## 3. Install Dependencies

Install the required dependencies using pip:

pip install -r requirements.txt

## 4. Start Docker Compose

Start the database service using Docker:

docker-compose up -d

This will set up the MySQL database as specified in the docker-compose.yml file.

## 5. Run the Application

Navigate to the app directory and start the FastAPI application:

cd app
python app.py

## 6. Access the API

Once the application is running, you can access the API documentation at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## Notes

Ensure Docker and Docker Compose are installed and running on your system.

Use the .env file to configure database connection settings as needed.
