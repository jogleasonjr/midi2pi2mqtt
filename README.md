## Midi-to-Pi-to-MQTT

Publish input from MIDI devices to MQTT using a Raspberry Pi. This allows you to map buttons, faders, and knobs to your home automation system. For example, I use this with a PadKontrol to control hue bulb brightness (knobs) and control a Volumio server (pad buttons). But any MIDI device should work.

The MQTT channel is sent json, so the consuming end can easily consume the properties of the MIDI message.

Last tested 2022-02-05 with a Raspberry Pi Zero W flashed with Raspian 11 (bullseye).

### Package Dependencies (apt install these)
* python3-pip
* libjack-dev

### Python Dependencies (pip install these)
* mido
* paho.mqtt
* python-rtmidi

### To Run

Edit `run.py` to, at a minimum, point to your MQTT server. Then run:

`python run.py`

Example output sent to your MQTT channel:

```
# Playing notes
{"event":"note_on","channel":"9","note":"67","velocity":"127","time":"0"}
{"event":"note_off","channel":"9","note":"67","velocity":"64","time":"0"}

# Turning knobs (note the "value" property changing)

{"event":"control_change","channel":"9","control":"20","value":"85","time":"0"}
{"event":"control_change","channel":"9","control":"20","value":"86","time":"0"}
{"event":"control_change","channel":"9","control":"20","value":"87","time":"0"}
{"event":"control_change","channel":"9","control":"20","value":"88","time":"0"}

# Extra data, in this case I'm changing scenes to 1, 2, then 3 on a Korg PadKontrol. Note the 0, 1, and 2 as the last element of the data array.
{"event":"sysex","data":"(66,64,110,8,95,79,0)","time":"0"}
{"event":"sysex","data":"(66,64,110,8,95,79,1)","time":"0"}
{"event":"sysex","data":"(66,64,110,8,95,79,2)","time":"0"}
```

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

### HomeAssistant Integration

Since this script sends json to the mqtt channel, HomeAssistant's mqtt triggers will automatically populate a `trigger.payload_json` object with the values from the MIDI controller. Here's an example automation I use that toggles a `switch`, toggles a `light`, and controls a `light` object's brightness with a control knob:

```yaml
alias: PadKontrol -> Office Lights
description: ''
trigger:
  - platform: mqtt
    topic: midi/pk
condition: []
action:
  - choose:
      - conditions:
          - condition: template
            value_template: >-
              {{trigger.payload_json.event == "note_on" and
              trigger.payload_json.note == "65"}}
        sequence:
          - service: switch.toggle
            data: {}
            target:
              entity_id: switch.tradfri_plug_02
      - conditions:
          - condition: template
            value_template: >-
              {{trigger.payload_json.event == "note_on" and
              trigger.payload_json.note == "59"}}
        sequence:
          - service: light.toggle
            data: {}
            target:
              entity_id: light.basement_desk_corner_light_level_on_off
      - conditions:
          - condition: template
            value_template: >-
              {{trigger.payload_json.event == "control_change" and
              trigger.payload_json.control == "20"}}
        sequence:
          - service: light.turn_on
            data:
              brightness: '{{ trigger.payload_json.value | int * 2 }}'
            target:
              entity_id: light.basement_desk_corner_light_level_on_off
    default: []
mode: single
```

### Node-RED Integration

Since this script publishes json the the mqtt channel, the default `mqtt in` node will parse this automatically, and you can reference properties of the object using, for example, `msg.payload.event` or `msg.payload.note`.
