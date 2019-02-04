#!/usr/bin/env python

import mido
import paho.mqtt.client as mqtt
import struct

print(mido.get_output_names())

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.jtpk.io", 1883, 60)

def print_message(message):
    b = message.bytes()
    ba = bytearray(b)
    client.publish("midi/pk/raw", payload=ba)
    print(message)

port = mido.open_input('padKONTROL:padKONTROL MIDI 2 20:1', callback=print_message)
port.callback = print_message

client.loop_forever()




# control_change channel=9 control=21 value=19 time=0
# note_on channel=9 note=56 velocity=127 time=0

