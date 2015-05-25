#**********Testing Phase************
import pickle
import math
import sys

def cosine_similarity(v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def Levenshtein_Distance(s, len_s, t, len_t):
  # base case: empty strings 
  if len_s == 0:
    return len_t;
  if len_t == 0:
    return len_s;
 
  # test if last characters of the strings match
  if s[len_s-1] == t[len_t-1]:
      cost = 0;
  else:
      cost = 1;
 
  # return minimum of delete char from s, delete char from t, and delete char from both 
  return min(Levenshtein_Distance(s, len_s - 1, t, len_t    ) + 1,
                 Levenshtein_Distance(s, len_s    , t, len_t - 1) + 1,
                 Levenshtein_Distance(s, len_s - 1, t, len_t - 1) + cost);

def Levenshtein_Similarity(s1, s2):
    return 1 - Levenshtein_Distance(s1, len(s1), s2, len(s2))/max(len(s1),len(s2))

def summerize_PAS(PAS_key):
    PAS_list = PAS_key.split()
    PAS_key = ''
    begin = False;
    for item in PAS_list:
        if item.startswith('S-'):
            PAS_key += item[2:]+' '
            begin = False
        elif item.startswith('B-'):
            PAS_key += item[2:]+' '
            begin = True
        elif ( item.startswith('I-') or item.startswith('E-') ) and begin:
            continue
        elif item.startswith('I-') and not begin:
            PAS_key += item[2:]+' '
            begin = True
        elif item.startswith('E-') and not begin:
            PAS_key += item[2:]+' '
            begin = False
    return PAS_key


def Calculate_Score(target_PAS_key, target_PAS_dic, intersection):
    target_PAS = ''
    true_target_PAS_dic = {}
    if not intersection == target_PAS_key:
        #print(target_PAS_dic)
        for item in target_PAS_key.split():
            if item in intersection:
                target_PAS += item+' '
        for PAS in target_PAS_dic:
            true_target_PAS = ''
            for item in PAS.split():
                if item in intersection:
                    true_target_PAS += item+' '
            true_target_PAS_dic[true_target_PAS]=target_PAS_dic[PAS]
    else:
        target_PAS = target_PAS_key
        true_target_PAS_dic = target_PAS_dic    
    #calculate weighted Levenshtein Similarity
    target_PAS_list = target_PAS.split()
    frequency_list = []
    total_similarity = 0
    for true_target in true_target_PAS_dic:
        true_target_list = true_target.split()
        freq = true_target_PAS_dic[true_target]
        frequency_list.append(freq)
        if true_target == '':
            print('hah???')
            continue
        total_similarity += Levenshtein_Similarity(target_PAS_list, true_target_list)*freq
    #print([total_similarity,sum(frequency_list),total_similarity/float(sum(frequency_list))])
    total_similarity = total_similarity/float(sum(frequency_list))
    #print('total_similarity: %d' %total_similarity)
    return total_similarity
    

def Get_Sentence_Score(sentence, verbs, sequence_alignment):
    if len(verbs)==0:# if sentence has no verb
        return 0.5
    score_list = []    
    for i in range(1,len(verbs)+1):#for each verb in this sentence
        verb_key = verbs[i-1]# get key verb for verbs_dic
        #source_PAS_key=[]
        source_PAS_key=''
        for token in sentence:#for each row of this column (verb)
            if not token[i+4]=='O':
                #source_PAS_key.append(token[i+4])
                source_PAS_key += token[i+4]+' '
        #target_PAS_key=[]
        target_PAS_key=''
        for number in sequence_alignment:#for each number in aligned list
            token = sentence[int(number)]
            if not token[i+4]=='O':
                #target_PAS_key.append(token[i+4])
                target_PAS_key+= token[i+4]+' '
        #summerize Source PAS
        source_PAS_key = summerize_PAS(source_PAS_key)
        #summerize target PAS 
        target_PAS_key = summerize_PAS(target_PAS_key)

        if verb_key in verbs_dic:
            source_PAS_dic = verbs_dic[verb_key]
            if source_PAS_key in source_PAS_dic:
                target_PAS_dic = source_PAS_dic[source_PAS_key]
                #calculate score
                score_list.append(Calculate_Score(target_PAS_key,target_PAS_dic,target_PAS_key))
            else:
                source_PAS_list = source_PAS_key.split()
                intersection = []
                match_PAS = ''
                for PAS in source_PAS_dic:
                    PAS_list = PAS.split()
                    new_intersection = [val for val in source_PAS_list if val in PAS_list]
                    indx = 0
                    while indx < len(source_PAS_list) and not source_PAS_list[indx] in PAS_list:
                        indx+=1
                    if indx == len(source_PAS_list):
                        continue
                    last_index=PAS_list.index(source_PAS_list[indx])
                    for item in new_intersection:
                        if PAS_list.index(item) > last_index:
                            last_index = PAS_list.index(item)
                        else:
                            new_intersection.remove(item)
                    if len(new_intersection) > len(intersection):
                        intersection = new_intersection
                        match_PAS = PAS
                if len(intersection) <= 1:# we consider there is not in the Data
                    score_list.append(0.5)
                    continue
                target_PAS_dic = source_PAS_dic[match_PAS]                
                #if intersection tags are less or equal than half of the true tags, we can ignore 
                #or maybe we can find similar PAS in similar verb types
                #calculate score according to intersection part
                score_list.append((len(intersection)/len(source_PAS_list))* Calculate_Score(target_PAS_key,target_PAS_dic,intersection))
        else: 
            #print('verb %s not found'%verb_key)
            score_list.append(0.5)
            continue
    #print(score_list)
    return sum(score_list) / float(len(score_list))

#Load Data from Training 
verbs_dic = pickle.load( open( "../Train/Data.p", "rb" ) )
if len(sys.argv)>1:
    test_Labeled_File = open('NIST.en.labeled.'+sys.argv[1],'r+')
    n_best_File = open('nbest-5000-withAlignment-'+sys.argv[1],'r+')
    new_n_best_File = open('new-nbest-5000-withAlignment-'+sys.argv[1],'w+')    
else:
    n_best_File = open('nbest-5000-withAlignment','r+')
    new_n_best_File = open('new-nbest-5000-withAlignment','w+')
n_best_count = 5000
sentence = []
verbs = []
alignedLine = n_best_File.readline()
(snum, csentence, features, tscore, alignment) = alignedLine.strip().split("|||")
sentence_number = int(snum)
while True:#read the whole labeled file
    line = test_Labeled_File.readline()
    if line == '':#reach the end of labeled file
        break
    elif line == '\n':#reach the end of a sentence in labeled file
        #print(sentence_number)
        n=0
        sys.stdout.write(str(sentence_number)+':')
        while int(snum) == sentence_number: 
            sys.stdout.write('%d,'%n)
            sys.stdout.flush()
            #read sequence number of alignment                        
            spAlign = alignment.split()
            alignNumbers=[]
            for s in spAlign:
                if '=' in s :#just to find out if this number is alignment or part of sentence
                    align = s.split('=')
                    if '-' in align[0]:
                        num_range = align[0].split('-')
                        for num in range(int(num_range[0]),int(num_range[1])+1):
                            alignNumbers.append(str(num))
                    else:
                        alignNumbers.append(align[0])
            #------------------------------------
            #Call Get_Sentence_Score
            score = Get_Sentence_Score(sentence,verbs,alignNumbers)
            new_n_best_File.write(snum+' ||| '+csentence+' ||| '+features+'SRL_1: '+str(score)+' ||| '+tscore+' ||| '+alignment+'\n')
            alignedLine = n_best_File.readline()
            (snum, csentence, features, tscore, alignment) = alignedLine.strip().split("|||")  
            n += 1                      
        sentence=[]
        verbs=[]
        sentence_number = int(snum)
        sys.stdout.write('\n')
        continue
    sp = line.split()
    if not sp[4]=='-':#count verbs in this sentence
        verbs.append(sp[4])
    sentence.append(sp)
print('-------------------------------------------')
test_Labeled_File.close()
n_best_File.close()
new_n_best_File.close()

