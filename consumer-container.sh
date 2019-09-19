#!/bin/bash
cd ./consumer/
docker build -t consumer .
docker-compose up