#!/usr/bin/env python
# FT 12/04/21
# Forwards images from the camera to the YOLO detector on request (so that YOLO can keep up).

import threading
import sys, rospy
from sensor_msgs.msg import Image
# Use an empty message to send a signal.
from std_msgs.msg import Empty

#def on_image(image):
#    if ((rospy.get_rostime()).nsecs - last_time_nsecs > pub_intv_nsecs):
#        last_time_nsecs = (rospy.get_rostime()).nsecs
#        image_pub.publish(image)

#pub_intv_nsecs = 1000000000 # Publish image every 4 seconds.
#last_time_nsecs = (rospy.get_rostime()).nsecs

# TODO Will these two block each other? Do I need multithreading? Could multithreading lead
# to a race condition s.t. a request is missed?

class RequestListener (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        print('Starting request listener thread')
        request_sub = rospy.Subscriber("trophy_image_request", Empty, on_request)

def on_image(image):
    global image_requested
    #if image_requested:
    #    image_pub.publish(image)
    #    print('Success')
    # If a new image has been requested:
    if image_requested:
        image_pub.publish(image)
        image_requested = False
        print('Published')

def on_request(request):
    global image_requested
    print("Request received")
    image_requested = True

image_requested = False

rospy.init_node('image_forwarder')
image_sub = rospy.Subscriber("camera1/image_raw", Image, on_image, queue_size=1)
image_pub = rospy.Publisher("image_for_trophy_detection", Image)

# Start request listener thread:
request_listener = RequestListener(1, "Request listener", 1)
request_listener.start()

# Keep alive
while not rospy.is_shutdown():
    rospy.spin()