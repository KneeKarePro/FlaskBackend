import influxdb_client_3 as influx 
from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# InfluxDB connection
client = influx.InfluxDBClient3(host="localhost", port=8086, token="my-token", org="my-org", debug=False)

