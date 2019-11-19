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
            for i in range(0,7):
                dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (dataPoint.__class__ is RawDataPoint):
                omindwave_value = int(dataPoint._readRawValue())

                # Rescale the value to match MIDI spec
                # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
                mindwave_value = int((((omindwave_value - -2048) * (15 - 0)) / (2048 - -2048)) + 0) * 8

                if mindwave_value > 64 or mindwave_value < 40:
                    print('RAW VALUE: {0}, MIDI VALUE: {1}'.format(omindwave_value, mindwave_value))
                    note_on = [0x90, mindwave_value, 112]
                    note_off = [0x80, mindwave_value, 0]
                    midiout.send_message(note_on)
                    midiout.send_message(note_off)
    del midiout
else:
    print('Error connecting to MindWave Mobile!')
    sys.exit(1)  
