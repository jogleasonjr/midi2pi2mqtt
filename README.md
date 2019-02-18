## Midi-to-Pi-to-MQTT

Publish input from MIDI devices to MQTT using a Raspberry Pi. This allows you to map buttons, faders, and knobs to your home automation system. For example, I use this with a PadKontrol to control hue bulb brightness (knobs) and control a Volumio server (pad buttons).

### Dependencies
* mido
* paho.mqtt.client

### To Run

`python run.py`

### To install as a systemd service

```bash
cp midi2pi2mqtt.service /lib/systemd/system
chmod 644 /lib/systemd/system/midi2pi2mqtt.service
systemctl enable midi2pi2mqtt
systemctl daemon-reload
systemctl start midi2pi2mqtt
```

### To view service logs (i.e. journal entries for this service)

`journalctl -u midi2pi2mqtt`

The `-f` switch for `journalctl` will follow/tail the logs.

### TODO

* Add installation script for service
* Add configuration options for the MIDI device,  MQTT host, and topic
* Add `systemd` logging
