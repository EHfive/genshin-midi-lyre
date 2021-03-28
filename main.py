from os import path
from threading import Thread
from time import sleep
from mido import MidiFile
import argparse
import keyboard as kbd

octave_interval = 12
c3_pitch = 48
c4_pitch = 60
c5_pitch = 72
c6_pitch = 84
keytable = "z?x?cv?b?n?m" + "a?s?df?g?h?j" + "q?w?er?t?y?u"

play_state = False

def play(midi, channels, octave, no_semi, shift):
    global play_state
    play_state = True
    print('Start playing')
    if not midi:
        midi = path.join(path.dirname(path.realpath(__file__)), 'files/canon.mid')

    for msg in MidiFile(midi):
        if not play_state:
            break

        sleep(msg.time)
        if msg.is_meta:
            continue

        if msg.type == 'note_on':
            if channels and not msg.channel in channels:
                continue

            note = msg.note + octave * octave_interval

            if note < c3_pitch:
                print('note {} lower than c3')
                if shift:
                    note = note % octave_interval + c3_pitch
            elif note >= c6_pitch:
                print('note {} higher than b5')
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

def control(args_dict):
    global play_state
    if play_state:
        play_state = False
    else:
        kbd.call_later(lambda: play(**args_dict), delay=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play midi file on Windsong Lyre in Genshin')
    parser.add_argument('midi', nargs="?", type=str, help='path to midi file')
    parser.add_argument('-c', '--channels', nargs="*", type=int, help="enabled midi channels")
    parser.add_argument('-o', '--octave', default=0, type=int, help="shift octave")
    parser.add_argument('--no-semi', action='store_true', help="don't shift black key to white key")
    parser.add_argument('--shift', action='store_true', help="shift notes which out of range")
    args = parser.parse_args()

    print('Press "win + /" to start/stop playing, press "backspace" to exit.\n')

    kbd.add_hotkey('win+/',
        lambda: control(vars(args)),
        suppress=True,
        trigger_on_release=True)
    kbd.wait('backspace', suppress=True)
