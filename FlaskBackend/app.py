import influxdb_client as influx 
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio

from datetime import datetime
import os

app = Flask(__name__)

def influx_db_setup(url: str | None, token: str | None, org: str | None) -> influx.InfluxDBClient:
    """
    The influx_db_setup function sets up the InfluxDB client.

    Returns:
        - The InfluxDB client
    """
    load_dotenv()
    url = url if url is not None else os.getenv("INFLUXDB_URL")
    # token = "b0D8NCvGSIupVSmCTwvZ7_JaQkM_ls-bcmcT72xojGNhftBIqDa5TLiIinrOvAVQNNyyaiu21ggbvN5CxRipFA==" # Linux Desktop
    token = token if token is not None else os.getenv("INFLUXDB_TOKEN")
    org = org if org is not None else os.getenv("INFLUXDB_ORG")
    write_client: InfluxDBClient = InfluxDBClient(url=url, token=token, org=org)

    # Test connection
    health: influx.HealthCheck = write_client.health()
    assert health.status == "pass", f"Connection failed: {health.message}"

    return write_client

def write_data_to_influxdb(data: pd.DataFrame, client: InfluxDBClient, bucket: str) -> None:
    """
    The write_data_to_influxdb function writes data to InfluxDB.

    Args:
        - data: The data to write to InfluxDB
        - client: The InfluxDB client
    """
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for index, row in data.iterrows():
        point = Point("angle") \
            .tag("sensor", row["sensor"]) \
            .field("angle", row["angle"]) \
            .time(datetime.now(), WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)

async def write_data_to_influxdb_async(data: pd.DataFrame, client: InfluxDBClient, bucket: str) -> None:
    """
    The write_data_to_influxdb function writes data to InfluxDB asynchronously.

    Args:
        - data: The data to write to InfluxDB
        - client: The InfluxDB client
    """
    write_api = client.write_api(write_options=ASYNCHRONOUS)
    for index, row in data.iterrows():
        point = Point("angle") \
            .tag("sensor", row["sensor"]) \
            .field("angle", row["angle"]) \
            .time(datetime.now(), WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)


@app.route("/write_data", methods=["POST"])
def write_data():
    """
    The write_data function writes data to InfluxDB.

    Returns:
        - The response
    """
    data = request.json
    data = pd.DataFrame(data)
    client = influx_db_setup(None, None, None)
    write_data_to_influxdb(data, client, "test")
    return jsonify({"message": "Data written successfully"})

"""
Get data from InfluxDB based on user name from the URL


"""
@app.route("/get_data/<username>", methods=["GET"])
def get_data(username):
    """
    The get_data function gets data from InfluxDB.

    Args:
        - username: The username to get data for

    Returns:
        - The response
    """
    client = influx_db_setup(None, None, None)
    query = f'from(bucket: "test") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "angle" and r.sensor == "{username}")'
    result = client.query_api().query(query)
    data = []
    for table in result:
        for record in table.records:
            data.append(record.values)
    return jsonify(data)

@app.route("/test_fake_data", methods=["GET"])
def test_fake_data():
    """
    The test_fake_data function returns fake data.

    Returns:
        - The response
    """
    df=pd.DataFrame(np.random.randint(0,90,size=(10, 2)), columns=['sensor', 'angle'])
    # Send data out to API

    data = df.to_dict(orient="records")
    jsonify(data)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()