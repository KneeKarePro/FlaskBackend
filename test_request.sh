#!/bin/bash

# Bash script for sending POST and GET requests to a server for testing

# Variables
CONTENT_TYPE="Content-Type: application/json"
URL="http://localhost:5000"

# Functions
post() {
    curl -X POST "$URL/data" -H "$CONTENT_TYPE" -d '{"username": "testuser", "angle": 45.0, "rotation": 89.0}'
}

get_all() {
    curl -X GET "$URL/data/testuser" -H "$CONTENT_TYPE"
}

get_stats() {
    curl -X GET "$URL/data/stats/testuser" -H "$CONTENT_TYPE"
}

delete_user() {
    curl -X DELETE "$URL/data/testuser" -H "$CONTENT_TYPE"
}

# Main script
case "$1" in
    post)
        post
        ;;
    get_all)
        get_all
        ;;
    get_stats)
        get_stats
        ;;
    delete_user)
        delete_user
        ;;
    *)
        echo "Usage: $0 {post|get_all|get_stats}"
        exit 1
        ;;
esac
