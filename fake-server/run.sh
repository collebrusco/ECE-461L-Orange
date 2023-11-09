docker build -t orange:fake-server --network=host .
docker run -d -p 8888:8888 --name fake-server orange:fake-server
