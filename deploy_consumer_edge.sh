#!/bin/bash
docker login -u pborges docker.mobiledgex.net
docker tag consumer docker.mobiledgex.net/mobile/images/producer:1.0
docker push docker.mobiledgex.net/mobile/images/consumer:1.0
docker logout docker.mobiledgex.net