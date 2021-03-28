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
b5_pitch = 83
keytable = "z?x?cv?b?n?m" + "a?s?df?g?h?j" + "q?w?er?t?y?u"

play_state = 'idle'

def help():
    print('Press "win + /" to start/stop playing, press "backspace" to exit.\n')


def play(midi, shift, no_semi, out_range):
    global play_state
    play_state = 'running'
    print('Start playing')
    for msg in midi:
        if play_state != 'running':
            break

        sleep(msg.time)

        if msg.type != 'note_on':
            continue

        note = msg.note + shift
        orig_note = note

        if note < c3_pitch:
            print('note {:<3} lower than C3 : {:+}'.format(note, c3_pitch - note))
            if out_range:
                note = note % octave_interval + c3_pitch
        elif note > b5_pitch:
            print('note {:<3} higher than B5: {:+}'.format(note, b5_pitch - note))
            if out_range:
                note = note % octave_interval + c5_pitch

        note -= c3_pitch

        if note < 0 or note >= 36:
            print("{:<3} -\n".format(orig_note))
            continue

        if keytable[note] == '?' and not no_semi:
            note -= 1
            orig_note -= 1
        key = keytable[note]
        print("{:<3} {}\n".format(orig_note, key))
        kbd.send(key)

    print('Stop playing')
    help()

    play_state = 'idle'


def control(*args):
    global play_state

    if play_state == 'running':
        play_state = 'stopping'
    elif play_state == 'idle':
        it = args[0]
        args = [it()] + list(args)[1:]
        kbd.call_later(
            lambda: play(*args),
            delay=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play midi file with Windsong Lyre in Genshin Impact')
    parser.add_argument('midi', nargs="?", type=str, help='path to midi file')
    parser.add_argument('-c', '--channels', nargs="*", type=int, help="enabled midi channels, available values:0, 1, 2,...,N")
    parser.add_argument('-s', '--shift', type=int, default=None, help="shift note pitch, auto calculated by default")
    parser.add_argument('--no-semi', action='store_true', help="don't shift black key to white key")
    parser.add_argument('--shift-out-of-range', dest="out_range", action='store_true', help="shift notes which out of range")
    args = parser.parse_args()

    midi = args.midi
    if not midi:
        midi = path.join(path.dirname(path.realpath(__file__)), 'files/canon.mid')
    midi = MidiFile(midi)
    it = lambda: midi_iter(midi, args.channels)

    shift = args.shift
    if shift == None:
        shift = find_best_shift(it())
        print('Auto calculated pitch shift: {} semitone(s)'.format(shift))

    kbd.add_hotkey('win+/',
        lambda: control(it, shift, args.no_semi, args.out_range),
        suppress=True,
        trigger_on_release=True)

    help()
    kbd.wait('backspace', suppress=True)
