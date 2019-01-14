#/* Copyright (C) Florentina Petcu - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Florentina Petcu <florentina.ptc@gmail.com>, December 2018
# */

from SPARQLWrapper import SPARQLWrapper, JSON
from googletrans import Translator
from updateOntology import *
from queryOntology import *
from translate import *


def main():
	f_read = open('../resources/synonyms.txt', 'r+')
	f_write = open('../resources/synonyms.txt', 'a+')
	sparqlQuery = SPARQLWrapper("http://localhost:3030/doid/query")
	sparqlUpdate = SPARQLWrapper("http://localhost:3030/doid/update")

	synonymColumn = getSynonymColumn(sparqlQuery)
	print(len(synonymColumn))
	content = [line.strip() for line in f_read]

	for synonym in synonymColumn:
		if synonym not in content:
			translatedSynonym = ''
			try:
				translatedSynonym = translateSynonym(synonym)
				translatedSynonym = translatedSynonym.replace('\"', '')
			except Exception as e:
				print (e)
				break
			if translatedSynonym != '':
				insertTranslation(sparqlUpdate, translatedSynonym, synonym)
			f_write.write(synonym + '\n')
			
	print(len(getTranslatedLabels(sparqlQuery)))
	f_read.close()
	f_write.close()

main()