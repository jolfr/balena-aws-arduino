##
# Code modified from boilerplate written by Daniel Andrade
# https://github.com/balena-io-playground/balena-aws-iot-mqtt-example
#
# By Jack Carroll
##

import time
import os
import base64
import serial

from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

### Functions

def payload_report(self, params, packet):
    print("----- New Payload -----")
    print("Topic: ", packet.topic)
    print("Message: ", packet.payload)
    print("-----------------------")

def set_cred(env_name, file_name):
    #Turn base64 encoded environmental variable into a certificate file
    env = os.getenv(env_name)
    with open(file_name, "wb") as output_file:
        output_file.write(base64.b64decode(env))

### MQTT Setup
certRootPath = '/usr/src/app/'
print("\nMQTT Thing Starting...\n")

aws_endpoint = os.getenv("AWS_ENDPOINT", "data.iot.us-east-1.amazonaws.com")
aws_port = os.getenv("AWS_PORT", 8883)
device_uuid = os.getenv("BALENA_DEVICE_UUID")

# Save credential files
set_cred("AWS_ROOT_CERT","root-CA.crt")
set_cred("AWS_THING_CERT","thing.cert.pem")
set_cred("AWS_PRIVATE_CERT","thing.private.key")

# Unique ID. If another connection using the same key is opened the previous one is auto closed by AWS IOT
mqtt_client = AWSIoTMQTTClient(device_uuid) 

#Used to configure the host name and port number the underneath AWS IoT MQTT Client tries to connect to.
mqtt_client.configureEndpoint(aws_endpoint, aws_port)

# Used to configure the rootCA, private key and certificate files. configureCredentials(CAFilePath, KeyPath='', CertificatePath='')
mqtt_client.configureCredentials(certRootPath+"root-CA.crt", certRootPath+"thing.private.key", certRootPath+"thing.cert.pem")

# Configure the offline queue for publish requests to be 20 in size and drop the oldest
mqtt_client.configureOfflinePublishQueueing(-1)

# Used to configure the draining speed to clear up the queued requests when the connection is back. (frequencyInHz)
mqtt_client.configureDrainingFrequency(2) 

# Configure connect/disconnect timeout to be 10 seconds
mqtt_client.configureConnectDisconnectTimeout(10)

# Configure MQTT operation timeout to be 5 seconds
mqtt_client.configureMQTTOperationTimeout(5)
 
# Connect to AWS IoT with default keepalive set to 600 seconds
mqtt_client.connect()

# Subscribe to the desired topic and register a callback.
mqtt_client.subscribe("balena/payload_test", 1, payload_report)

# Open serial connection to Arduino
print("Serial Port Connecting...\n")
ser = serial.Serial("/dev/ttyACM0", 9600)   #TODO add error checking for ACM port

print("Setup complete! Will begin publishing now\n")
i=0
while True:
    if ser.in_waiting != 0:
        i = float(ser.readline())
        print('Analog sensor value to publish: ', i)
        mqtt_client.publish("arduino/analog_sensor", i, 0)