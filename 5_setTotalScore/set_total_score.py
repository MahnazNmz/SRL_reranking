import operator

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

n_best_File = open('/home/mahnaz/Desktop/pipeline/Test Corpora/nbest-5000-withAlignment','r+')
weight_File = open('/home/mahnaz/Desktop/pipeline/Test Corpora/weight.txt','r')
new_n_best_File = open('nbest-5000-withAlignment-rescored','w+')

weights=[]
while True:#read the whole weight file
	line = weight_File.readline()
	if line == '':
		break
	weights.append(float(line))    
print(weights)

count = 1
while True:#read the whole n-best file
	line = n_best_File.readline()
	if line == '':
		break
	(i, sentence, features, totalScore, alignment) = line.strip().split("|||")
	featureScores = []
	for h in features.strip().split():
		if(isfloat(h)):
			featureScores.append(float(h))
	totalScore = sum(map( operator.mul, featureScores, weights))
	#print(totalScore)	
	new_n_best_File.write(i+' ||| '+sentence+' ||| '+features+' ||| '+str(totalScore)+' ||| '+alignment+'\n')
n_best_File.close()
weight_File.close()
new_n_best_File.close()
