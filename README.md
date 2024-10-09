# Flask Backend

The backend for both our web app and mobile app for monitoring and processing Knee rehabilitation data

## Usage

The project uses poetry as the package dependency and build management system.

To run the backend, first install poetry and clone the repository. After cloning and entering the repository directory, run `poetry install` to install the required dependencies for production and development.

After installing the dependencies, run `poetry run python FlaskBackend/app.py` to start the backend server. The server will be running on `127.0.0.1:5000`.

## API

The API is a RESTful API that uses the Flask framework to handle requests. The API is used to interact with the SQLite database to store and retrieve data from the database.

### Endpoints
1. `/data` - POST request to store data in the database
   1. Request Body:
      ```json
      {
        "username": "user_id",
        "angle": 0.0,
        "rotation": 0.0,
      }
      ```
    2. Response:
        ```json
        {
          "status": "success",
          "message": "Data stored successfully"
        }
        ```
2. `/data/<username>` - GET request to retrieve data from the database
    1. Response:
        ```json
        {
          "status": "success",
          "data": [
            {
              "angle": 0.0,
              "rotation": 0.0,
              "timestamp": "2021-09-01 12:00:00"
            },
            {
              "angle": 0.0,
              "rotation": 0.0,
              "timestamp": "2021-09-01 12:00:01"
            }
          ]
        }
        ```
    2. Response:
        ```json
        {
          "status": "error",
          "message": "No data found"
        }
        ```
3. `/data/range/<username>` - GET request to retrieve data from the database within a range
    1. Request Parameters:
        - `start`: Start date in the format `YYYY-MM-DD`
        - `end`: End date in the format `YYYY-MM-DD`
    2. Response:
        ```json
        {
          "status": "success",
          "data": [
            {
              "angle": 0.0,
              "rotation": 0.0,
              "timestamp": "2021-09-01 12:00:00"
            },
            {
              "angle": 0.0,
              "rotation": 0.0,
              "timestamp": "2021-09-01 12:00:01"
            }
          ]
        }
        ```
    3. Response:
        ```json
        {
          "status": "error",
          "message": "No data found"
        }
        ```
4. `/data/stats/<username>` - GET request to retrieve statistics from the database
    1. Response:
        ```json
        {
          "angle": {
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0
          },
          "rotation": {
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0
          }
        }
        ```
5. `/data/<username>` - DELETE request to delete data from the database
    1. Response:
        ```json
        {
          "message": "Data deleted"
        }
        ```
    2. Response:
        ```json
        {
          "error": "Data not found"
        }
        ```
## Framework

The project use the Flask framework for settings up backend API Routes for both of our Web App and Mobile App. The primary function of our backend is working within InfluxDB to query and process our temporal data from our users to be displayed within there account. There are two sets of API calls, one for the mobile application which focuses on summary data, and the other for more complex analytics on our web app.

### Flask

### SQLite

---

## Developing

### Poetry

In order to setup the developer environment, first install [poetry](https://python-poetry.org/) and clone this repository. After cloning and entering the repository directory, run `poetry install` to install the required dependencies for production and development.