# Flask Backend

The backend for both our web app and mobile app for monitoring and processing Knee rehabilitation data

## Usage

The project uses poetry as the package dependency and build management system.

## Framework

The project use the Flask framework for settings up backend API Routes for both of our Web App and Mobile App. The primary function of our backend is working within InfluxDB to query and process our temporal data from our users to be displayed within there account. There are two sets of API calls, one for the mobile application which focuses on summary data, and the other for more complex analytics on our web app.

### Flask

### InfluxDB
InfluxDB is a time series database that is used to store our user's data. The data is stored in a bucket that is unique to each user. The data is stored in the following format:
```
measurement: knee_data
tags: user_id
fields: x, y, z, timestamp
```
The data is stored in the following format to allow for easy querying and processing of the data. The data is stored in a time series format to allow for easy querying of the data.

First install the InfluxDB database and then install the Influx CLI. The Influx CLI is used to create the database and the bucket for the data. The following commands are used to create the database and the bucket:
```
influx setup \
  --force \
  --username my-user \
  --password my-password \
  --org my-org \
  --bucket my-bucket \
  --retention 1w
```

---

## Developing

### Poetry

In order to setup the developer environment, first install [poetry](https://python-poetry.org/) and clone this repository. After cloning and entering the repository directory, run `poetry install` to install the required dependencies for production and development.

### Environment Variables

Our **InfluxDB** database credentials are stored within the following variables:
- INFLUXDB_URL=XXX
- INFLUXDB_TOKEN=XXX
- INFLUXDB_ORG=XXX

It is recommended the environment variables be stored within some environment variable management system like a `.env` file which will be loaded by the backend anyways. The format for the `.env` file looks as such:
```
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=my-token
INFLUXDB_ORG=my-org
```
The values are example values and need to be adjusted to match the production or development configuration
