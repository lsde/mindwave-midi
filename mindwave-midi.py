#!/usr/bin/env python3
import sys, os
import time
import bluetooth
import rtmidi
from mindwavemobile.MindwaveDataPoints import RawDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader

mindwaveDataPointReader = MindwaveDataPointReader(address=os.environ['MINDWAVE_MAC'])
mindwaveDataPointReader.start()

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    try:
        midiout.open_port(1)
    except rtmidi._rtmidi.InvalidPortError:
        midiout.open_virtual_port("mindwave-midi")

if (mindwaveDataPointReader.isConnected()):    
    with midiout:
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (dataPoint.__class__ is RawDataPoint):
                omindwave_value = int(dataPoint._readRawValue())
                mindwave_value = int((((omindwave_value - -2048) * (127 - 0)) / (2048 - -2048)) + 0)
                print(omindwave_value, mindwave_value)

                note_on = [0x90, mindwave_value, 112]
                note_off = [0x80, mindwave_value, 0]

                midiout.send_message(note_on)
                #time.sleep(0.05)
                midiout.send_message(note_off)
                #time.sleep(0.05)
    del midiout
else:
    print('Error connecting to MindWave Mobile!')
    sys.exit(1)  