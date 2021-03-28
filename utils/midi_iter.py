from mido import MidiFile

def midi_iter(midi: MidiFile, channels):
    for msg in midi:
        if msg.is_meta:
            continue
        if channels and not msg.channel in channels:
            continue
        yield msg

