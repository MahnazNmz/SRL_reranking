#**********Training Phase************
import pickle

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

labeledFile = open('/home/mahnaz/MyDrive/Uni/Python/FeatureExtraction/corpus.true.en.labeled','r+')
alignmentFile = open('/home/mahnaz/MyDrive/Uni/Python/FeatureExtraction/en.fa.alignment.txt','r')
sentence_counter=1
verbs=[]
sentence=[]
verbs_dic={}
while True:#read the whole file
    line = labeledFile.readline()
    if line=='':#reach the end of file
        break
    elif line=='\n':#reach the end of a sentence
        #read sequence number of alignment
        firstLine = alignmentFile.readline()
        s_t_length = [int(s) for s in firstLine.split() if s.isdigit()]
        if not s_t_length[1]==len(sentence):
            print([sentence_counter, s_t_length[1], len(sentence)])
        alignmentFile.readline()
        alignLine = alignmentFile.readline()
        spAlign= alignLine.split()
        alignNumbers=[]
        for s in spAlign:
            if s=='({':#just to find out if this number is alignment or part of sentence
                start=1
            elif s=='})':
                start=0
            if any(i.isdigit() for i in s) and start==1:
                alignNumbers.append(s)
        #------------------------------------
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
            for number in alignNumbers:#for each number in aligned list
                token = sentence[int(number)-1]
                if not token[i+4]=='O':
                    #target_PAS_key.append(token[i+4])
                    target_PAS_key+= token[i+4]+' '

            #summerize Source PAS
            source_PAS_key = summerize_PAS(source_PAS_key)
            #summerize target PAS 
            target_PAS_key = summerize_PAS(target_PAS_key)

            #insert in the verbs_dic
            if verb_key in verbs_dic:
                sourcePAS_dic = verbs_dic.get(verb_key)
                if source_PAS_key in sourcePAS_dic:
                    targetPAS_dic = sourcePAS_dic.get(source_PAS_key)
                    if target_PAS_key in targetPAS_dic:
                        targetPAS_dic[target_PAS_key]=targetPAS_dic[target_PAS_key]+1
                    else:
                        targetPAS_dic[target_PAS_key]=1
                else:
                    targetPAS_dic={}
                    targetPAS_dic[target_PAS_key]=1
                    sourcePAS_dic[source_PAS_key]=targetPAS_dic
            else:
                targetPAS_dic={}
                targetPAS_dic[target_PAS_key]=1
                sourcePAS_dic={}
                sourcePAS_dic[source_PAS_key]=targetPAS_dic
                verbs_dic[verb_key]=sourcePAS_dic
            #print('%d|| verb:%s source_PAS_key:%s target_PAS_key:%s' %(sentence_counter, verb_key, source_PAS_key, target_PAS_key))
        sentence=[]
        verbs=[]
        sentence_counter+=1
        continue
    sp = line.split()
    if not sp[4]=='-':#count verbs in this sentence
        verbs.append(sp[4])
    sentence.append(sp)
print('-------------------------------------------')
print('total verbs: %d'%len(verbs_dic))
labeledFile.close()
alignmentFile.close()
#Read Data to file
pickle.dump( verbs_dic, open( "Data.p", "wb" ) )
load_dic = pickle.load( open( "Data.p", "rb" ) )