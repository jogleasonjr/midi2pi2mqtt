#!/usr/bin/env python

import mido
import paho.mqtt.client as mqtt
import struct


# TODO: Add as startup args
mqtt_server = "mqtt.jtpk.io"
mqtt_port = 1883
mqtt_topic = "midi/pk"
midi_attached_device = "padKONTROL:padKONTROL MIDI 2 20:1"

print("Discovered MIDI devices:")
print(mido.get_output_names())

# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# Callback for messages sent to the topic
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


# Create an object from the raw midi message and publish serialized JSON to the topic
def publish_to_mqtt_topic(message):
    kvps = ("event=" + str(message)).split(" ")
    json = {k: v for kvp in kvps for k, v in (kvp.split("="),)}
    json_str = str(json).replace("'", '"')
    client.publish(mqtt_topic, payload=json_str)
    print(json_str)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_server, mqtt_port, 60)

port = mido.open_input(midi_attached_device)
port.callback = publish_to_mqtt_topic

client.loop_forever()
