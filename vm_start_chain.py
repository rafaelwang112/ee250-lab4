#Team Members: Rafael Wang
#GitHub Repo: https://github.com/rafaelwang112/ee250-lab4

import paho.mqtt.client as mqtt
import time

pingpong_number = 1 #variable to keep track of the number
prev_number = 0 #variable just to prevent republishing the same number before the new number is received

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc)) #Confirmation of acknowledgement response from server
    client.subscribe("rafaelwa/pong") #subscribe to pong subtopic (topic in cont_chain)

    client.message_callback_add("rafaelwa/pong", on_message_from_ponginfo) #custom callback

def on_message_from_ponginfo(client, userdata, message): #custom message callback for pong
    global pingpong_number #to be able to change global variable value inside this func.
    pingpong_number = int(message.payload.decode()) #cast as int
    print ("Pong: " + str(pingpong_number))
    pingpong_number = pingpong_number+1 #update the value


if __name__ == '__main__':
    client = mqtt.Client() #create a client object
    client.on_connect = on_connect #attach on_connect() func

    client.connect(host="172.20.10.2", port=1883, keepalive=60) #my RPi address

    client.loop_start() #spawn thread
    time.sleep(4) #give a couple seconds to ensure both clients are connected before first publish

    while True:
        if pingpong_number != prev_number: #to ensure same number isn't published multiple times
            time.sleep(1)
            client.publish("rafaelwa/ping", pingpong_number)
            prev_number = pingpong_number #update prev_number