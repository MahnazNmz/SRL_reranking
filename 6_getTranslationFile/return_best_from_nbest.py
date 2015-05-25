#nbest_File = open('/home/mahnaz/Desktop/pipeline/Test Corpora/nbest-5000-withAlignment','r+')
nbest_File = open('/home/mahnaz/MyDrive/Uni/Python/FeatureExtraction/set-total-score/nbest-5000-withAlignment-sorted','r+')
translationFile = open('/home/mahnaz/MyDrive/Uni/Python/FeatureExtraction/get-Translation-File/best_translation_rescored.fa','w')
nbest_count = 5000
sentenceNum=0
line = nbest_File.readline()
spline = line.split(' ||| ')
while True:	
	if line == '':
		break
	sentence = spline[1]
	translationFile.write(sentence+'\n')
	#for i in range(1,nbest_count-1):
	while int(spline[0])==sentenceNum:
		line = nbest_File.readline()
		spline = line.split(' ||| ')
	sentenceNum += 1
nbest_File.close()
translationFile.close()
