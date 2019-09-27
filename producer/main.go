package main

import (
	"encoding/json"
	"fmt"
	"image"
	"io"
	"log"
	"os"
	"time"
	"github.com/Shopify/sarama"
	"github.com/adaickalavan/kafkapc"
	"gocv.io/x/gocv"
)

//Hooks that may be overridden for testing
var inputReader io.Reader = os.Stdin
var outputWriter io.Writer = os.Stdout

// Instantiate a producer
var producer sarama.AsyncProducer

// Instantiate the Kafka topic
var ntopic string = "test"

// Instantiate the RSTP Link
var rstp_link = "rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream"

func main() {
	//Sarama logger
	sarama.Logger = log.New(outputWriter, "[saramaLog]", log.Ltime)

	//Create a Kafka producer
	var brokers = []string{"kafka:9093"}
	var err error
	producer, err = kafkapc.CreateKafkaProducer(brokers)
	if err != nil {
		panic("Failed to connect to Kafka. Error: " + err.Error())
	}
	//Close producer to flush(i.e., push) all batched messages into Kafka queue
	defer func() { producer.Close() }()

	// Capture video
	webcam, err := gocv.OpenVideoCapture(rstp_link)
	if err != nil {
		panic("Error in opening webcam: " + err.Error())
	}

	// Stream images from RTSP to Kafka message queue
	frame := gocv.NewMat()
	for {
		if !webcam.Read(&frame) {
			continue
		}

 		resultImage := gocv.NewMatWithSize(512, 288, gocv.MatTypeCV8U)
		gocv.Resize(frame, &resultImage, image.Pt(resultImage.Rows(), resultImage.Cols()), 0, 0, gocv.InterpolationCubic)

		// Type assert frame into RGBA image
		imgInterface, err := resultImage.ToImage()
		if err != nil {
			panic(err.Error())
		}
		img, ok := imgInterface.(*image.RGBA)
		if !ok {
			panic("Type assertion of pic (type image.Image interface) to type image.RGBA failed")
		}

		//Form the struct to be sent to Kafka message queue
		doc := Result{
			Pix:      img.Pix,
			Channels: frame.Channels(),
			Rows:     frame.Rows(),
			Cols:     frame.Cols(),
		}

		//Prepare message to be sent to Kafka
		docBytes, err := json.Marshal(doc)
		if err != nil {
			log.Fatal("Json marshalling error. Error:", err.Error())
		}
		msg := &sarama.ProducerMessage{
			Topic:     ntopic,
			Value:     sarama.ByteEncoder(docBytes),
			Timestamp: time.Now(),
		}
		//Send message into Kafka queue
		producer.Input() <- msg

		//Print time of receiving each image to show the code is running
		fmt.Fprintf(outputWriter, "Sending Camera 1 Bytes ---->>>> %v\n", time.Now())
	}
}

//Result represents the Kafka queue message format
type Result struct {
	Pix      []byte `json:"pix"`
	Channels int    `json:"channels"`
	Rows     int    `json:"rows"`
	Cols     int    `json:"cols"`
}
