
import echonest.remix.audio as audio
import loader
import random
import os


def mix(start=None, seg=None, base=None, volume=0.3, pan=0.):
    # this assumes that the audios have the same frequency/numchannels
    startsample = int(start * seg.sampleRate)
    seg = seg[0:]
    seg.data *= (volume-(pan*volume), volume+(pan*volume)) # pan + volume
    if base.data.shape[0] - startsample > seg.data.shape[0]:
        base.data[startsample:startsample+len(seg.data)] += seg.data[0:]
    return base

def is_in(val, ls):
    for e in ls:
        if abs(e - val) < 0.01:
            return True
    return False

def insert_sfx(song_path):
    paths = ['bin' + os.sep + f for f in os.listdir('bin')]
    cowbell_paths = filter(lambda a: 'cowbell' in a, paths)
    cowbells = [audio.AudioData(path, sampleRate = 44100, numChannels = 2) for path in cowbell_paths]
    # other_paths = filter(lambda a: 'cowbell' not in a, paths)
    # others = [audio.AudioData(path, sampleRate = 44100, numChannels = 2) for path in other_paths]
    song = audio.LocalAudioFile(song_path)
    beats = song.analysis.beats
    tatums = song.analysis.tatums
    bars = song.analysis.bars
    beats_raw = [b.start for b in beats]
    tatums_raw = [t.start for t in beats]
    bars_raw = [b.start for b in bars]
    for tatum in tatums:
        if random.random() > 0.75:
            continue
        if is_in(tatum.start, bars_raw):
            song = mix(tatum.start, random.choice(cowbells), song)
        elif is_in(tatum.start, beats_raw) and random.random() < 0.75:
            song = mix(tatum.start, random.choice(cowbells), song)
        elif random.random() < 0.3:
            song = mix(tatum.start, random.choice(cowbells), song)
    return song
    
        
if __name__ == '__main__':
    song = insert_sfx('/home/kevin/Music/top100/36 Anaconda.mp3')
    song.encode('/home/kevin/Music/test.mp3')
