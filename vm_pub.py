#Team Members: Rafael Wang
#GitHub Repo: https://github.com/rafaelwang112/ee250-lab4

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
    #get IP address
    ip_address=0 
    hostname = socket.gethostname() #retrieve local machine hostname
    ip_address = socket.gethostbyname(hostname) # translate hostname into ip address
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python.
        
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    while True:
        client.publish("rafaelwa/ipinfo", f"{ip_address}")
        print("Publishing ip address")
        time.sleep(4)

        my_datetime = datetime.now() #create datetime instance
        my_date = my_datetime.date() #get date
        my_time = my_datetime.time() #get time

        #publish date and time in their own topics
        client.publish("rafaelwa/dateinfo", f"{my_date}")
        print("Publishing date")
        client.publish("rafaelwa/timeinfo", f"{my_time}")
        print ("Publishing time")