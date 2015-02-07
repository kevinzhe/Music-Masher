# load songs to audiodata objects

def loadSongs(*args):
    songs = []
    for path in args:
        if type(path) != str: raise TypeError
        try: open(path) 
        except: raise TypeError
    for path in args:
        song = audio.LoadLocalAudioFile(path)
        songs.append(song)
    return songs
