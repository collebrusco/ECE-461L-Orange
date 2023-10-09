# Build docker image
docker build -t orange:frontend --network=host .

# Build static files using frontend container
docker run --name frontend orange:frontend

# Copy static files to backend directory
docker cp frontend:/frontend/build ../flask_container
