"""
Test the Connection to InfluxDB

The InfluxDB is our database for storing the temporal data. This test checks the connection to the InfluxDB as well other operations like writing data to the database, reading data from the database, etc. 

The test cases are written using the pytest framework.
"""
import pytest
import influxdb_client_3 as influx
from dotenv import load_dotenv
import os

load_dotenv()

# Test the connection to the InfluxDB
def test_connection():
    # Get the environment variables
    url = os.getenv("INFLUXDB_URL")
    token = os.getenv("INFLUXDB_TOKEN")
    org = os.getenv("INFLUXDB_ORG")
    bucket = os.getenv("INFLUXDB_BUCKET")

    # Create a client
    client = influx.InfluxDBClient3(host=url, token=token, org=org, bucket=bucket)

    # Test the connection
    query: str = "from(bucket: \"{}\") |> range(start: -1h)".format(bucket)
    assert client.query(query=query, language="flux") is not None
