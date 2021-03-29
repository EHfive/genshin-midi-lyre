
def midi_play_filter(msg, channels):
    if msg.is_meta or msg.type != 'note_on':
        return False
    if channels and not msg.channel in channels:
        return False
    return True

