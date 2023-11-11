#!/bin/bash
clear
# Set environment variables for this subshell
  export MONGO_HOST=localhost
  export MONGO_PORT=27017
  export MONGO_USERNAME=root
  export MONGO_PASSWORD=examplepassword
  export MONGO_AUTHDB=admin
  export MONGO_DB=admindb  

# Start a subshell
(
    python -m pytest tests/
)



