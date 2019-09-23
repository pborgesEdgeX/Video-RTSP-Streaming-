#!/bin/bash
if [ -z "$1" ]
  then
    printf "No username supplied.\nRetry running: ./deploy_producer_edge.sh <USERNAME>\n"
    exit 1
fi
docker login -u $1 docker.mobiledgex.net
docker tag producer docker.mobiledgex.net/mobile/images/producer:1.0
docker push docker.mobiledgex.net/mobile/images/producer:1.0
docker logout docker.mobiledgex.net