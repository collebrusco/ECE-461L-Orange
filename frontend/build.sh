# Build docker image
docker build -t orange:frontend --network=host .

# Deploy using frontend container
docker run -d -p 3000:3000 --name frontend orange:frontend
