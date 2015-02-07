import echonest.remix.audio as audio
#import echonest.remix.modify as modify
import dirac


def newTempo(song, oldTempo, newTempo):
    # ratio = newTempo / oldTempo
    ratio = oldTempo / newTempo
    scaled = dirac.timeScale(song.data, ratio)
    out = audio.AudioData(ndarray = scaled, shape = scaled.shape,
                sampleRate = song.sampleRate, numChannels = scaled.shape[1])
    return out
