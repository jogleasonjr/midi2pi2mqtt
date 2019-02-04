## Midi-to-Pi-to-MQTT

Publish MIDI messages to MQTT using a Raspberry Pi.

### Dependencies


### To Run

`python run.py`

### To install as a systemd service

`cp midi2pi2mqtt.service /lib/systemd/system`
`chmod 644 /lib/systemd/system/midi2pi2mqtt.service`
`systemctl enable midi2pi2mqtt`
`systemctl daemon-reload`
`systemctl start midi2pi2mqtt`

### To view service logs (i.e. journal entries for this service)

`journalctl -u midi2pi2mqtt`

The `-f` switch for `journalctl` will follow/tail the logs.

### TODO

* Add configuration option for the MIDI device
* Add configuration options for the MQTT host and topic
* Add `systemd` logging
