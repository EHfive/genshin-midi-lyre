# Genshin MIDI Lyre
Play midi file with Windsong Lyre.

## Requirements

* Genshin Impact(原神) on Windows
* Python 3
* `keyboard` module
* `mido` module
* Git (optional)

## Install

```
git clone https://github.com/EHfive/genshin-midi-lyre.git
cd genshin-midi-lyre
pip install -r .\requirements.txt
```

## Usage

```
> python .\main.py --help
usage: main.py [-h] [-c [CHANNELS ...]] [-s SHIFT] [--no-semi] [--shift-out-of-range] [midi]

Play midi file with Windsong Lyre in Genshin Impact

positional arguments:
  midi                  path to midi file

optional arguments:
  -h, --help            show this help message and exit
  -c [CHANNELS ...], --channels [CHANNELS ...]
                        enabled midi channels, available values:0, 1, 2,...,N
  -s SHIFT, --shift SHIFT
                        shift note pitch, auto calculated by default
  --no-semi             don't shift black key to white key
  --shift-out-of-range  shift notes which out of range
```

1. Start Genshin Impact(原神)
2. Equipt Windsong Lyre
3. Press Z (or your custom keymap) to use Windsong Lyre
4. Run `admin_cmd.bat` to get an administrator cmd terminal
5. Run `python main.py [path to midi file]` in administrator terminal

## Credits

"canon.mid" & "admin_cmd.bat" are borrowed from https://github.com/Misaka17032/genshin-lyre-auto-play
