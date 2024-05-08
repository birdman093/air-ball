#!/bin/sh

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 953243985013.dkr.ecr.us-east-2.amazonaws.com
docker build -t air-ball-v0 .
docker tag air-ball-v0:latest 953243985013.dkr.ecr.us-east-2.amazonaws.com/air-ball-ecr:latest
docker push 953243985013.dkr.ecr.us-east-2.amazonaws.com/air-ball-ecr:latest

