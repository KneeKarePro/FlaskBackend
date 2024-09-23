# Flask Backend

The backend for both our web app and mobile app for monitoring and processing Knee rehabilitation data

## Usage

The project uses poetry as the package dependency and build management system.

## Framework

The project use the Flask framework for settings up backend API Routes for both of our Web App and Mobile App. The primary function of our backend is working within InfluxDB to query and process our temporal data from our users to be displayed within there account. There are two sets of API calls, one for the mobile application which focuses on summary data, and the other for more complex analytics on our web app.

### Flask

### SQLite

---

## Developing

### Poetry

In order to setup the developer environment, first install [poetry](https://python-poetry.org/) and clone this repository. After cloning and entering the repository directory, run `poetry install` to install the required dependencies for production and development.

### Environment Variables
