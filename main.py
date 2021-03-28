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
notetable = "C?D?EF?G?A?B"

play_state = 'idle'


def help():
    print('Press "\\" to start/stop playing, press "backspace" to exit.\n')


def note_name(note):
    idx = note % octave_interval
    if idx < 0:
        return '-'
    pre = notetable[idx]
    if pre == '?':
        pre = notetable[idx - 1] + '#'
    return pre + str(note // octave_interval - 1)


def print_note(ch, orig, play, key):
    print("ch {:<2}  orig: {:<3}{:<5}  play: {:<3}{:<5}    {}\n"
            .format(ch, note_name(orig),
                    '(' + str(orig) + ')',
                    note_name(play) if play else '-',
                    '(' + str(play) + ')' if play else '-',
                    key if key else '-'))


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
            print(
                'note {:<3} lower than C3 : {:+}'.format(note, c3_pitch - note))
            if out_range:
                note = note % octave_interval + c3_pitch
        elif note > b5_pitch:
            print(
                'note {:<3} higher than B5: {:+}'.format(note, b5_pitch - note))
            if out_range:
                note = note % octave_interval + c5_pitch

        if note < c3_pitch or note > b5_pitch:
            print_note(msg.channel, orig_note, None, None)
            continue

        if keytable[note - c3_pitch] == '?' and not no_semi:
            note -= 1
        key = keytable[note - c3_pitch]
        print_note(msg.channel, orig_note, note, key.upper())
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
    parser = argparse.ArgumentParser(
        description='Play midi file with Windsong Lyre in Genshin Impact')
    parser.add_argument('midi', nargs="?", type=str, help='path to midi file')
    parser.add_argument('-c', '--channels', nargs="*", type=int,
                        help="enabled midi channels, available values:0, 1, 2,...,N")
    parser.add_argument('-s', '--shift', type=int, default=None,
                        help="shift note pitch, auto calculated by default")
    parser.add_argument('--no-semi', action='store_true',
                        help="don't shift black key to white key")
    parser.add_argument('--shift-out-of-range', dest="out_range",
                        action='store_true', help="shift notes which out of range")
    args = parser.parse_args()

    midi = args.midi
    if not midi:
        midi = path.join(path.dirname(
            path.realpath(__file__)), 'files/canon.mid')
    midi = MidiFile(midi)
    def it(): return midi_iter(midi, args.channels)

    shift = args.shift
    if shift == None:
        shift = find_best_shift(it())
        print('Auto calculated pitch shift: {} semitone(s)\n'.format(shift))

    kbd.add_hotkey('\\',
                   lambda: control(it, shift, args.no_semi, args.out_range),
                   suppress=True,
                   trigger_on_release=True)

    help()
    kbd.wait('backspace', suppress=True)
