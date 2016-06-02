import sys
from practnlptools.tools import Annotator
import nltk


def preprocessor(mail):
	mail = mail.replace('(','[').replace(')',']')
	return mail



def detector(mail,outputfileName):

	annotator=Annotator()
	sentences = nltk.sent_tokenize(mail)
	probableActionItemSentences = []
	for sentence in sentences:
		text = nltk.word_tokenize(sentence)
		posTags = nltk.pos_tag(text)
		for tags in posTags:
			if tags[1]=="VB":
				probableActionItemSentences.append(sentence)
				break
	for sentence in probableActionItemSentences:
		srLabels = annotator.getAnnotations(sentence)['srl']
		#print(srLabels)
		depParsedContent = annotator.getAnnotations(sentence,dep_parse=True)
		#print(depParsedContent)
		root = depParsedContent['dep_parse']
		root = root[root.find('root('):]
		root = root[:root.find('\n')]
		root = root[root.find(',')+2:root.rfind('-')]
		parsedList = depParsedContent['srl']
		owner = None
		ownerFound = False
		for parsedMap in parsedList:
			if 'V' in parsedMap and parsedMap['V'] == root:
				if 'A0' in parsedMap:
					owner = parsedMap['A0']
					ownerFound = True
				else:
					owner = 'You'
					ownerFound = True
				break
		if not ownerFound:
			for parsedMap in parsedList:
				if 'A0' in parsedMap:
					ownerFound = True
					if parsedMap['A0'].lower() == 'you' or parsedMap['A0'].lower() == 'we' or parsedMap['A0'].lower() == 'us':
						owner = parsedMap['A0']
						ownerFound = True
						break
		if ownerFound and owner==None:
			print("")
		else:
			
			outputfile.write("OWNER : "+owner+" SENTENCE : "+sentence+"\n")
			



mailFile = sys.argv[1]
outputfileName = sys.argv[2]
outputfile = open(outputfileName, 'a+')
outputfile.write("FILE NAME : "+mailFile)
with open(mailFile) as inputFile:
	mail = inputFile.read()
mail = preprocessor(mail)
detector(mail,outputfileName)
outputfile.close()

