package kafkapc

import (
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/Shopify/sarama"
	"github.com/wvanbergen/kafka/consumergroup"
)

type messageHandler func(*sarama.ConsumerMessage) error

//ConsumerParam contains the consumer connection properties
type ConsumerParam struct {
	GroupName string   //ConsumerGroup name
	Topics    []string //Topic name
	Zookeeper []string //Zookeeper 'IP:Port' address
}

//ConsumeMessages creates consumer group to consume the messages
func ConsumeMessages(consumerParam ConsumerParam, handler messageHandler) {
	log.Println("Starting Consumer")
	config := consumergroup.NewConfig()
	config.Offsets.Initial = sarama.OffsetOldest
	config.Offsets.ProcessingTimeout = 10 * time.Second

	//Create a consumer within a consumer group
	consumer, err := consumergroup.JoinConsumerGroup(
		consumerParam.GroupName,
		consumerParam.Topics,
		consumerParam.Zookeeper,
		config)
	if err != nil {
		log.Fatal("Failed to join consumer group:", consumerParam.GroupName, err)
	}

	//Relay incoming signals to channel 'c'
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	signal.Notify(c, os.Kill)

	//Terminate the consumer gracefully upon receiving a kill signal.
	go func() {
		<-c
		if err := consumer.Close(); err != nil {
			log.Println("Error closing the consumer:", err)
		}

		log.Println("Consumer closed.")
		os.Exit(0)
	}()

	//Read from the Errors() channel to avoid consumer deadlock
	go func() {
		for err := range consumer.Errors() {
			log.Println("Consumer deadlock detected:", err)
		}
	}()

	//Consume messages from Kafka queue
	log.Println("Waiting for messages")
	for message := range consumer.Messages() {
		log.Printf("Topic: %s\t Partition: %v\t Offset: %v\n", message.Topic, message.Partition, message.Offset)
		//Only take messages from subscribed topic
		//Potentially perform different operations on messages from different topics
		switch message.Topic {
		case consumerParam.Topics[0]:
			//Handle the message
			e := handler(message)
			if e != nil {
				log.Fatal("Error in handling consumed message:", e)
				consumer.Close()
			} else {
				//Mark the message as processed
				consumer.CommitUpto(message)
			}
		}
	}
}
