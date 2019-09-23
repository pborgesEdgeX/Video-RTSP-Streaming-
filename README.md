# RTSP Video Streaming Application - From Producer to Consumer

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

For you to build this code successfully, make sure you have the following installed:

```
# Python 3.6
$ python3 --version
Python 3.6.5

# Docker
$ docker --version
Docker version 19.03.2, build 6a30dfc

# Docker Compose
$ docker-compose --version
docker-compose version 1.24.1, build 4667896b

# java
$ java -version
openjdk version "12.0.2" 2019-07-16
OpenJDK Runtime Environment (build 12.0.2+10)
OpenJDK 64-Bit Server VM (build 12.0.2+10, mixed mode, sharing)

$ pip3 --version
pip 19.1.1

$ virtualenv --version
16.7.2

```
### Tested Environment
Operating system:
 --> macOS Mojave 10.14.3 (18D109)

### Overall Architecture
With this demo, we are building an application of a complete producer to consumer video streaming. We picked the sample video from a RTSP source via URL to be streamed via a Producer inside the full_app-dockerNet network. The producer is written in Go with the purpose of efficiently sending frames to the Kafka pipe. Keep in mind some image resizing is needed to ensure the pipe doesn't overload and Sarama lib avoids throwing an exception. In this app, we have two consumers. One consumer runs inside the container network talking to the Kafka pipe through kaka:9093 port. The other is designed to be run from the localhost accessing the Kafka pipe via localhost:9092. In both cases, we generated a docker image and a local environment containing the same packages mostly including popular Computer Vision framework (OpenCV) and popular ML/DL frameworks (TF, Keras, Theano and Caffe).

![Alt text](readme_img/output.jpg?raw=true "Output")

### Installing

In order to get your code up and running, first let's clone the repo locally then compose the project:

```
$ cd <PATH_OF_CHOICE>
$ git clone https://github.com/pborgesEdgeX/full_app.git
$ cd full_app/
$ docker-compose up
```

When you execute the docker compose command, the producer, Kafka pipe and consumers containers will be created and begin to execute. You should see an output similar to this:

![Alt text](readme_img/kafka_architecture.jpg?raw=true "System Architecture")
 

At this point, you may want to run a consumer from your localhost. In this case, you should utilize our bash script:

```
$ chmod u+x consumer-localhost.sh
$ ./consumer-localhost.sh
```
This will run the producer locally.

## Running 

Once the system is up and running, you can see the consumers running on a Flask powered web-server.

The consumer inside the Docker network can be accessed: http://0.0.0.0:5001

The consumer running from the localhost can be accessed: http://0.0.0.0:5000

## Deployment on Edge Servers

If you wish to deploy your producer on Edge servers provisioned by MobiledgeX, you can use the following bash script:

```
$ chmod u+x deploy_producer_edge.sh
$ ./deploy_producer_edge.sh <USERNAME>
```

The same applies to the consumer:

```
$ chmod u+x deploy_consumer_edge.sh
$ ./deploy_consumer_edge.sh <USERNAME>
```

## Built With

* [Sarama](https://godoc.org/github.com/Shopify/sarama) - Package sarama is a pure Go client library for dealing with Apache Kafka (versions 0.8 and later).
* [Kafka Apache](http://wurstmeister.github.io/kafka-docker/) - Kafka pipelining
* [Flask](https://palletsprojects.com/p/flask/) - Consumer Web Server
* [OpenCV] (https://docs.opencv.org/) - Computer Vision Library in Consumer
* [Keras] (https://keras.io/) - Deep Learning API in Consumer

## Versioning

We use [SemVer](http://semver.org/) for versioning. The latest version of this code is 1.0.0.

## Authors

* **Paulo Borges** - *Initial work* - [MobiledgeX](https://github.com/pborgesEdgeX)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/pborgesEdgeX/full_app/blob/master/LICENSE) file for details

