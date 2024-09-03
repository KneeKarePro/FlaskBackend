# Flask Backend

The backend for both our web app and mobile app for monitoring and processing Knee rehabilitation data

## Usage

The project uses poetry as the package dependency and build management system.

## Framework

The project use the Flask framework for settings up backend API Routes for both of our Web App and Mobile App. The primary function of our backend is working within InfluxDB to query and process our temporal data from our users to be displayed within there account. There are two sets of API calls, one for the mobile application which focuses on summary data, and the other for more complex analytics on our web app.

### Flask

### InfluxDB

---

## Developing

### Poetry

In order to setup the developer environment, first install [poetry](https://python-poetry.org/) and clone this repository. After cloning and entering the repository directory, run `poetry install` to install the required dependencies for production and development.

### Environment Variables

Our **InfluxDB** database credentials are stored within the following variables:
- INFLUXDB_URL=XXX
- INFLUXDB_TOKEN=XXX
- INFLUXDB_ORG=XXX
- INFLUXDB_BUCKET=XXX

It is recommended the environment variables be stored within some environment variable management system like a `.env` file which will be loaded by the backend anyways. The format for the `.env` file looks as such:
```
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=my-token
INFLUXDB_ORG=my-org
INFLUXDB_BUCKET=my-bucket
```
The values are example values and need to be adjusted to match the production or development configuration
