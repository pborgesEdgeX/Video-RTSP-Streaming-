import sys
import time
import cv2
from kafka import KafkaProducer

topic = "distributed-video"

def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.

    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Open file
    video = cv2.VideoCapture(video_file)

    print('Publishing video sample...')

    while (video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break

        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)
        buffer.resize()
        print(buffer.tobytes())

        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())

        time.sleep(0)
    video.release()
    print('publish complete')


def publish_camera():

    """
    Publish camera video stream to specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """


    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Start up Producer 2
    producer2 = KafkaProducer(bootstrap_servers='localhost:9092')

    camera = cv2.VideoCapture('jellyfish-5-mbps-hd-h264.mkv')
    start_time = time.time()
    x = 1  # displays the frame rate every 1 second
    counter = 0
    print('Step 1')
    try:
        while (True):
            # Start counter
            #start_time = time.time()
            print('Step 2')
            success, frame = camera.read()
            print('Step 3')
            ret, buffer = cv2.imencode('.jpg', frame)
            print('Step 4')
            producer.send(topic, buffer.tobytes())
            print('Step 5')
            if (time.time() - start_time) > x:
                print("FPS: ", counter / (time.time() - start_time))
                counter = 0
                start_time = time.time()
            counter += 1
            producer2.send(topic, buffer.tobytes())


            #print("FPS: ", 1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop
            # Choppier stream, reduced load on processor
            time.sleep(0.1)
            print('Step 6')

    except:
        print("\nExiting.")
        camera.release()
        sys.exit(1)



if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg.
    Otherwise it will default by streaming webcam feed.
    """
    if (len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print('New app')
        print("publishing sample feed!")
        publish_camera()
