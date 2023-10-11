#!/bin/bash
docker build -t orange:backend .
docker run -p 8888:80 orange:backend

