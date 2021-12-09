#!/usr/bin/env python
"""Play a fixed frequency sound."""
from __future__ import division
import math
import random

from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

def sine_tone(frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                    channels=1, # mono
                    rate=sample_rate,
                    output=True)

    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)

    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()

def saw_tone(frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                    channels=1, # mono
                    rate=sample_rate,
                    output=True)

    def s(t):
        return volume * ((t * frequency / sample_rate) % 2 - 1)

    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()

TONES = {
    "a"  : 440.00,
    "a+" : 466.1,
    "b"  : 493.9,
    "c"  : 261.6,
    "c+" : 277.2,
    "d"  : 293.6,
    "d+" : 311.2,
    "e"  : 329.6,
    "f"  : 349.2,
    "f+" : 370.0,
    "g"  : 392.0,
    "g+" : 415.3,
}

def scale(base_note):

    keys = list(TONES.keys())
    index = keys.index(base_note)

    scale = [keys[index]]

    # two steps
    index += 2
    scale.append(keys[index % len(keys)])

    index += 2
    scale.append(keys[index % len(keys)])

    # half step
    index += 1
    scale.append(keys[index % len(keys)])

    # three steps
    index += 2
    scale.append(keys[index % len(keys)])

    index += 2
    scale.append(keys[index % len(keys)])

    index += 2
    scale.append(keys[index % len(keys)])

    # half step
    index += 1
    scale.append(keys[index % len(keys)])

    return scale



def play(tones, dur=1):

    for t in tones:
        tone = TONES[t]
        saw_tone(
            # see http://www.phy.mtu.edu/~suits/notefreqs.html
            frequency=TONES[t], # Hz, waves per second A4
            duration=dur, # seconds to play sound
            volume=.2, # 0..1 how loud it is
            # see http://en.wikipedia.org/wiki/Bit_rate#Audio
            sample_rate=22050 # number of samples per second
        )

def randomizer(tones, steps, dur=1):

    for i in range(steps):
        idx = random.randint(0, len(tones)-1)
        key = tones[idx]
        key2 = tones[(idx+2) % len(tones)]
        key3 = tones[(idx+4) % len(tones)];
        saw_tone(
            # see http://www.phy.mtu.edu/~suits/notefreqs.htmlhttp;
            frequency=TONES[key]+TONES[key2]+TONES[key3], # Hz, waves per second A4
            duration=dur, # seconds to play sound
            volume=.2, # 0..1 how loud it is
            # see http://en.wikipedia.org/wiki/Bit_rate#Audio
            sample_rate=22050 # number of samples per second
        )


#play("cccedddfeeddc", 1)

#play(scale("a"), 1)

randomizer(scale("c+"), 16)


#while(True):
#    sine_tone(
#        # see http://www.phy.mtu.edu/~suits/notefreqs.html
#        frequency=440.00, # Hz, waves per second A4
#        duration=1, # seconds to play sound
#        volume=.1, # 0..1 how loud it is
#        # see http://en.wikipedia.org/wiki/Bit_rate#Audio
#        sample_rate=22050 # number of samples per second
#    )
#
#    saw_tone(
#        # see http://www.phy.mtu.edu/~suits/notefreqs.html
#        frequency=440.00, # Hz, waves per second A4
#        duration=1, # seconds to play sound
#        volume=.1, # 0..1 how loud it is
#        # see http://en.wikipedia.org/wiki/Bit_rate#Audio
#        sample_rate=22050 # number of samples per second
#    )
