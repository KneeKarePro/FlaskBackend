# Make file for sending POST and GET requests to a server for testing
#

# Variables
CONTENT_TYPE = "Content-Type: application/json"
URL = "http://localhost:5000"

# Commands
post:
	curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"username": "testuser", "angle": 45.0, "rotation": 89.0}'

get:
	curl -X GET http://127.0.0.1:5000/data/testuser -H "Content-Type: application/json"
