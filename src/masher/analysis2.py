import echonest.remix.audio as audio
import featureAnalysis
import time

def getClosestBar(filename):
	song0 = audio.LocalAudioFile("dhorse1.wav")
	song = audio.LocalAudioFile(filename)
	sections = song.analysis.sections
	bars = song.analysis.bars
	sectionStart = [q.start for q in sections][1:]
	barStart = [b.start for b in bars]
	VIPBars = []
	for start in sectionStart:
		for i in xrange(len(barStart)-1):
			if barStart[i] < start and barStart[i+1] >= start:
				VIPBars += [i]
	#need to split the audio file based on the bar partitiion now
	for barVal in VIPBars:
		if barVal == VIPBars[0]: continue
		smallBar = audio.getpieces(song,bars[barVal-3:barVal+3])
		smallBar.encode("smallBar.wav")
		smallBar = audio.LocalAudioFile("smallBar.wav")
		print smallBar.analysis.segments
		return featureAnalysis.main(smallBar,song0)

# print getClosestBar("clock1.wav")

def compareSum(a,b):
	if sum(a) < sum(b): return -1
	else: return 1

def getSequence(f1,f2):
	song1 = audio.LocalAudioFile(f1)
	song2 = audio.LocalAudioFile(f2)
	sections1 = song1.analysis.sections
	sections2 = song2.analysis.sections
	A1 = [s.mean_loudness() for s in sections1]
	A2 = [s.mean_loudness() for s in sections2]
	# A1 = [featureAnalysis.loudnessMetric(s) for s in sections1]
	# A2 = [featureAnalysis.loudnessMetric(s) for s in sections2]
	sorted1 = sorted(sections1)[::-1]
	sorted2 = sorted(sections2)
	newList = []
	for i in xrange(len(sorted1)+len(sorted2)-1):
		newList += sorted1[i/2] if i%2 == 0 else sorted2[i/2]
	result = []
	# print len(sections1)
	counter = 0
	for s in newList:
		counter += 1
		if counter == 9:
			counter = 0
			time.sleep(0.5)
		s.encode("subsection.wav")
		t = audio.LocalAudioFile("subsection.wav")
		beats = t.analysis.beats
		result += [(t,beats)]
	return result


	# for i in xrange(len(sorted1)+len(sorted2)-1):

	# 	if i%2 == 0:
	# 		result += [sorted1[i/2]]
	# 	else:
	# 		result += [sorted2[i/2]]
	# return result

print getSequence("dhorse1.wav","clock1.wav")


