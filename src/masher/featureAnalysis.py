#get comparison metrics
import echonest.remix.audio as audio
import numpy as np
from changeToCorrectTempo import changeToCorrectTempo

# t1 = audio.LocalAudioFile("dhorse.wav").analysis.tempo["value"]
# t2 = audio.LocalAudioFile("clock.wav").analysis.tempo["value"]
# targetT = (t1+t2)*1.0/2
# changeToCorrectTempo("dhorse.wav",targetT).encode("dhorse1.wav")
# changeToCorrectTempo("clock.wav",targetT).encode("clock1.wav")
#loudness metric
def loudnessMetric(song1):
	# song1 = audio.LocalAudioFile(file1)
	chunks1 = song1.analysis.beats
	gradient = []
	for i in xrange(len(chunks1)-1):
		dif = chunks1[i+1].mean_loudness() - chunks1[i].mean_loudness()
		time = chunks1[i].duration
		gradient += [dif/time]
	assert(len(gradient) == len(chunks1)-1)
	return gradient

def getTime(filename):
	song = audio.LocalAudioFile(filename)
	chunks = song.analysis.beats
	time = [(chunks[index].start + chunks[index].duration/2) for index in xrange(len(chunks))]
	return time

def loudnessCMP(file1,file2,width=10,threshold=5):
	gradient1 = loudnessMetric(file1)
	gradient2 = loudnessMetric(file2)
	#want them to align when they are 0
	gradPoints1 = []
	gradPoints2 = []
	extr = None
	for i in xrange(len(gradient1)):
		extr = None
		if -1*threshold <= gradient1[i] <= threshold:
			if sum(gradient1[max(i-width,0):i]) <= 0 and sum(gradient1[i:min(i+width,len(gradient1))]) >= 0: extr = "min"
			elif sum(gradient1[max(i-width,0):i]) >= 0 and sum(gradient1[i:min(i+width,len(gradient1))]) <= 0: extr = "max"
			if extr != None: gradPoints1 += [(i,extr)]
	for j in xrange(len(gradient2)):
		extr = None
		if -1*threshold <= gradient2[j] <= threshold:
			if sum(gradient2[max(j-width,0):j]) <= 0 and sum(gradient2[j:min(j+width,len(gradient2))]) >= 0: extr = "min"
			elif sum(gradient2[max(j-width,0):j]) >= 0 and sum(gradient2[j:min(j+width,len(gradient2))]) <= 0: extr = "max"
			if extr != None: gradPoints2 += [(j,extr)]
	# print gradPoints1
	# print gradPoints2
	pairs = []
	time1 = getTime(file1)
	time2 = getTime(file2)
	for i in xrange(len(gradPoints1)):
		for j in xrange(len(gradPoints2)):
			if gradPoints1[i][1] == gradPoints2[j][1]:
				# pairs += [(time1[i],time2[j])]
				pairs += [(i,j)]
	return set(pairs)

def almostEqual(a,b,d=30):
	if abs(a-b) <= d: return True
	else: return False




def CMP(t1,t2):
	if t1[2] < t2[2]: return 1
	else: return -1

def pitchCmp(song1,song2,compare=CMP):
	# song1 = audio.LocalAudioFile(file1)
	# song2 = audio.LocalAudioFile(file2)
	chunks1 = song1.analysis.beats
	chunks2 = song2.analysis.beats
	closeVals = []
	for i in xrange(len(chunks1)):
		for j in xrange(len(chunks2)):
			vec1 = np.array(chunks1[i].mean_pitches())
			vec1 /= (np.dot(vec1,vec1)**0.5)
			vec2 = np.array(chunks2[j].mean_pitches())
			vec2 /= (np.dot(vec2,vec2)**0.5)
			result = np.dot(vec1,vec2)
			# closeVals += [(chunks1[i].start,chunks2[j].start,result)]
			closeVals += [(i,j,result)]
	closeVals = sorted(closeVals,compare)[:1000]
	closeVals = [(a[0],a[1]) for a in closeVals]
	return set(closeVals)

def timbreCMP(song1,song2,compare=CMP):
	# song1 = audio.LocalAudioFile(file1)
	# song2 = audio.LocalAudioFile(file2)
	chunks1 = song1.analysis.beats
	chunks2 = song2.analysis.beats
	closeVals = []
	for i in xrange(len(chunks1)):
		for j in xrange(len(chunks2)):
			vec1 = np.array(chunks1[i].mean_timbre())
			vec1 /= (np.dot(vec1,vec1)**0.5)
			vec2 = np.array(chunks2[j].mean_timbre())
			vec2 /= (np.dot(vec2,vec2)**0.5)
			result = np.dot(vec1,vec2)
			# closeVals += [(chunks1[i].start,chunks2[j].start,result)]
			closeVals += [(i,j,result)]
	closeVals = sorted(closeVals,compare)[:1000]
	closeVals = [(a[0],a[1]) for a in closeVals]
	return set(closeVals)

def intersection(s1,s2,eq=almostEqual):
	newSet = set([])
	for a in s1:
		for b in s2:
			if eq(a[0],b[0]) and eq(a[1],b[1]):
				newSet.add(a)
				print a
	return newSet

def main(song1,song2):
	# song1 = audio.LocalAudioFile(f1)
	# song2 = audio.LocalAudioFile(f2)
	l = loudnessCMP(song1,song2)
	p = pitchCmp(song1,song2)
	t = timbreCMP(song1,song2)
	matchup = intersection(intersection(l,p),t)
	return sorted(list(matchup))

# main("dhorse1.wav","clock1.wav")



# print loudnessCMP("dhorse.wav","clock.wav",5)
# print pitchCmp("dhorse.wav","clock.wav")
# print len(pitchCmp("dhorse.wav","clock.wav"))
# print len(loudnessCMP("dhorse.wav","clock.wav"))
# s= intersection(intersection(pitchCmp("dhorse1.wav","clock1.wav"),loudnessCMP("dhorse1.wav","clock1.wav")),timbreCMP("dhorse1.wav","clock1.wav"))
# print sorted(list(s))



