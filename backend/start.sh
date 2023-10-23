#!/bin/bash
docker build -t flask_backend .
docker run -p 8888:80 flask_backend

