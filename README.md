# RTSP Video Streaming Application - From Producer to Consumer

## Getting Started

These instructions provide you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
* macOS Mojave 10.14.3 (18D109)

### Overall Architecture
With this demo, we are building a complete producer to consumer application for video streaming. We picked the sample video from an RTSP source via URL streamed via a Producer inside the full_app-dockerNet network. The producer is written in Go to send frames to the Kafka pipe in the most efficient manner. Keep in mind some image resizing is needed to ensure the pipe doesn't overload and Sarama lib avoids throwing an exception. In this app, we have two consumers. One consumer runs inside the container network talking to the Kafka pipe through kaka:9093 port. The other is designed to be run from the localhost accessing the Kafka pipe via localhost:9092. In both cases, we generated a docker image and a local environment containing the same packages mostly including popular Computer Vision framework (OpenCV) and popular ML/DL frameworks (TF, Keras, Theano and Caffe).

![Alt text](readme_img/kafka_architecture.jpg?raw=true "Architecture")

### Installing

To get your code up and running, first let's clone the repo locally then compose the project:

```
$ cd <PATH_OF_CHOICE>
$ git clone https://github.com/pborgesEdgeX/full_app.git
$ cd full_app/
$ docker-compose up
```

When you execute the docker-compose command, the producer, Kafka pipe, and consumers containers are created and begin to execute. You should see an output similar to this:

![Alt text](readme_img/output.jpg?raw=true "Output")
 

At this point, you may want to run a consumer from your localhost. In this case, you should utilize our bash script:

```
$ chmod u+x consumer-localhost.sh
$ ./consumer-localhost.sh
```
These commands run the producer locally.


## Running 

Once the system is up and running, you can see the consumers running on a Flask powered web-server.

The consumer **inside the Docker network** can be accessed: http://0.0.0.0:5001

The consumer **running from the localhost** can be accessed: http://0.0.0.0:5000

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

## Adding your Algorithms
If you wish to modify the consumer, go ahead and cd into the /consumer folder. In there, you can find the main.py file. Add your own custom ML/DL algorithms where you have direct access to the image pixels in the get_stream() function:
```
feed = msg.value.get("pix")
```

Or Bytes: 
```
b = bytes(feed, 'utf-8')
```
## Modules included in Consumers

* darknet       latest (git)
* python        3.6    (apt)
* torch         latest (git)
* chainer       latest (pip)
* mxnet         latest (pip)
* onnx          latest (pip)
* pytorch       latest (pip)
* tensorflow    latest (pip)
* theano        latest (git)
* keras         latest (pip)
* lasagne       latest (git)
* opencv        4.0.1  (git)
* sonnet        latest (pip)
* caffe         latest (git)
* cntk          latest (pip)
* flask		latest (pip)
* numpy		latest (pip)
* dlib		latest (pip)
* facial-recognition latest (pip)
* Jinja2 	latest (pip)
* pyMongo	latest (pip)
* h5py		latest (pip)

## Troubleshooting
If you find any issues creating a topic, you can repeat the installation process and create a topic manually. To do so, go ahead with the following commands:

First, make sure sure you have the Kafka container up and running (your container should have a different ID than mine):

![Alt text](readme_img/containerup.jpg?raw=true "Container Check")

Now, it's time to access the Kafka container:

```
$ docker exec -i -t -u root $(docker ps | grep full_app_kafka | cut -d' ' -f1) /bin/bash
```
And manually create a topic (one single line command):
```
$ KAFKA_HOME/bin/kafka-topics.sh --create --partitions 4 --bootstrap-server kafka:9092 --replication-factor 1 --topic test
```
If you choose to monitor you consumer from within the container, you can do it so by manually creating a consumer:
```
$ KAFKA_HOME/bin/kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=test 
```
## Built With

* [Sarama](https://godoc.org/github.com/Shopify/sarama) - Package sarama is a pure Go client library for dealing with Apache Kafka (versions 0.8 and later).
* [Kafka Apache](http://wurstmeister.github.io/kafka-docker/) - Kafka pipelining
* [Flask](https://palletsprojects.com/p/flask/) - Consumer Web Server
* [OpenCV](https://docs.opencv.org/) - Computer Vision Library in Consumer
* [Keras](https://keras.io/) - Deep Learning API in Consumer
* [Deepo](https://hub.docker.com/r/ufoym/deepo/) - Series of Deep Learning Frameworks

## Versioning

We use [SemVer](http://semver.org/) for versioning. The latest version of this code is 1.0.0.

## Authors

* **Paulo Borges** - *Initial work* - [MobiledgeX](https://github.com/pborgesEdgeX)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/pborgesEdgeX/full_app/blob/master/LICENSE) file for details

