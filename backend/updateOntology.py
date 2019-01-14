#/* Copyright (C) Florentina Petcu - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Florentina Petcu <florentina.ptc@gmail.com>, December 2018
# */

from SPARQLWrapper import SPARQLWrapper, JSON


def insertTranslation(sparql, valueRo, valueEn):
	query = """ 
	INSERT { 
		?uri <http://www.w3.org/2002/07/rdfs#label> "%s"@ro
	} 
	WHERE { 
		?uri <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> "%s"
	} 
	"""%(valueRo, valueEn)
	
	sparql.setQuery(query) 
	sparql.method = 'POST'
	result = sparql.query()

	return result