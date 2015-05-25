import collections

n_best_File = open('nbest-5000-withAlignment-rescored','r+')
sorted_n_best_file = open('nbest-5000-withAlignment-sorted','w+')
sentenceNum = 0
score_list = {}
while True:
	line = n_best_File.readline()
	if line == '':
		#Last Sentence list	
		sorted_list = collections.OrderedDict(sorted(score_list.items(), reverse=True))
		for k, v in sorted_list.items():
			sorted_n_best_file.write(v)
		break
	spline = line.strip().split("|||")
	if int(spline[0])==sentenceNum:
		score_list[float(spline[3])]=line
	else:
		sorted_list = collections.OrderedDict(sorted(score_list.items(), reverse=True))
		for k, v in sorted_list.items():
			sorted_n_best_file.write(v)
		score_list = {}
		sentenceNum += 1

n_best_File.close()
sorted_n_best_file.close
#d = {2:3, 1:89, 4:5, 3:0}
#sd = collections.OrderedDict(sorted(d.items()))
#for k, v in sd.items():
#	print(v)
