import optparse
import math
from sys import stdout

optparser = optparse.OptionParser()
optparser.add_option("-s", "--split", dest="splitNum", default=7, help="number of split(s)")
optparser.add_option("-c", "--sentence-count", dest="sentenceCount", default=1045, help="number of sentences in test/dev file")
(opts, _) = optparser.parse_args()

splitNum = int(opts.splitNum)
sentenceCount = int(opts.sentenceCount)
sentences_per_split = math.ceil(sentenceCount/splitNum)
print(sentences_per_split)

labeled_File = open('NIST.en.labeled','r+')
scount = 1
sNum = 0
line = 'something'
while True:
#for j in range(0,):
	if line == '':
		break
	labeled_split = open('NIST.en.labeled.'+str(scount),'w+')
	for i in range(0,sentences_per_split):
		line = labeled_File.readline()
		if line == '':
			break
		stdout.write(str(i)+', ')
		while not line=='\n':
			labeled_split.write(line)
			line = labeled_File.readline()
			if line == '':
				break
		if line == '\n':
			labeled_split.write(line)
	print('--------------')
	scount += 1
	

    

