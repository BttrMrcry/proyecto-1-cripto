#!/bin/bash

docker build -t crypto .
docker run -t -d --name runner crypto
docker exec runner python runners.py
docker exec runner python graphics.py
docker cp runner:/crypto-runner/results ./results
docker cp runner:/crypto-runner/plots ./plots
docker stop runner
docker rm runner
docker image rm crypto