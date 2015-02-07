# Author: Kevin Zheng
# Created: 2/7/15

import echonest.remix.audio as audio
import echonest.remix.modify as modify
import numpy as np
import copy


def remove_vocals(song):
    '''give it a AudioData file, it'll return one w/ vocals removed'''
    if not issubclass(song.__class__, audio.AudioData):
        print 'Got %s, expected AudioData' % type(song)
        raise TypeError
    # new array of same size
    bg_only = copy.deepcopy(song)
    # out_shape = (len(song.data),)
    # bg_only = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
    # iterate though old song
    for sample in bg_only.data:
        new = sample[0] / 2 - sample[1] / 2
        sample[0] = new
        sample[1] = new

    return bg_only

    # # there should be a numpy iterator here
    # for x in np.nditer(data.song, flags=['external_loop'], order='F'):
    #     bg_only.data


if __name__ == '__main__':
    song = audio.LocalAudioFile('/home/kevin/Dropbox/TartanHacks2015/red.mp3')
    removed = remove_vocals(song)
    removed.encode('/home/kevin/Dropbox/TartanHacks2015/red-test-remove.mp3')