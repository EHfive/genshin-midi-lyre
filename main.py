from os import path
from threading import Thread
from time import sleep
from mido import MidiFile
import argparse
import keyboard as kbd
from utils import find_best_shift, midi_iter

octave_interval = 12
c3_pitch = 48
c4_pitch = 60
c5_pitch = 72
c6_pitch = 84
keytable = "z?x?cv?b?n?m" + "a?s?df?g?h?j" + "q?w?er?t?y?u"

play_state = False

def play(midi, shift, no_semi, out_range):
    global play_state
    play_state = True
    print('Start playing')
    for msg in midi:
        if not play_state:
            break

        sleep(msg.time)

        if msg.type != 'note_on':
            continue

        note = msg.note + shift

        if note < c3_pitch:
            print('note {} lower than c3'.format(note))
            if shift:
                note = note % octave_interval + c3_pitch
        elif note >= c6_pitch:
            print('note {} higher than b5'.format(note))
            if shift:
                note = note % octave_interval + c5_pitch

        note -= c3_pitch

        if note < 0 or note >= 36:
            continue

        if keytable[note] == '?' and not no_semi:
            note -= 1
        key = keytable[note]
        print("{:<3} {}\n".format(note, key))
        kbd.send(key)

    print('Stop playing')
    play_state = False

def control(midi, channels, shift, no_semi, out_range):
    global play_state
    if play_state:
        play_state = False
    else:
        if not midi:
            midi = path.join(path.dirname(path.realpath(__file__)), 'files/canon.mid')
        midi = MidiFile(midi)

        it = lambda: midi_iter(midi, channels)
        if shift == None:
            shift = find_best_shift(it())
        midi
        kbd.call_later(
            lambda: play(it(), shift, no_semi, out_range),
            delay=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play midi file on Windsong Lyre in Genshin')
    parser.add_argument('midi', nargs="?", type=str, help='path to midi file')
    parser.add_argument('-c', '--channels', nargs="*", type=int, help="enabled midi channels")
    parser.add_argument('-s', '--shift', type=int, default=None, help="shift note pitch, auto calculated by default")
    parser.add_argument('--no-semi', action='store_true', help="don't shift black key to white key")
    parser.add_argument('--shift-out-of-range', dest="out_range", action='store_true', help="shift notes which out of range")
    args = parser.parse_args()

    print('Press "win + /" to start/stop playing, press "backspace" to exit.\n')

    kbd.add_hotkey('win+/',
        lambda: control(**vars(args)),
        suppress=True,
        trigger_on_release=True)
    kbd.wait('backspace', suppress=True)
