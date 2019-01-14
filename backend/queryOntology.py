#/* Copyright (C) Florentina Petcu - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Florentina Petcu <florentina.ptc@gmail.com>, December 2018
# */

from SPARQLWrapper import SPARQLWrapper, JSON


def getSynonymColumn(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	query = """
	SELECT DISTINCT ?uri ?hasExactSynonym {
		?uri <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> ?hasExactSynonym
	}
	"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	synonymResults = []
	for result in results["results"]["bindings"]:
		synonymResults += [result["hasExactSynonym"]["value"]]

	return synonymResults

def getTranslatedLabels(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	query = """
	SELECT DISTINCT ?uri ?hasExactSynonym ?label {
		?uri <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> ?hasExactSynonym .
  		?uri <http://www.w3.org/2002/07/rdfs#label> ?label 
  		FILTER (langMatches(lang(?label), "ro" )) 
	}
	"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	translatedResults = {}
	for result in results["results"]["bindings"]:
		translatedResults[result["uri"]["value"]] = (result["hasExactSynonym"]["value"], result["label"]["value"])

	return translatedResults

def getAllergy(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	# query = """
	# SELECT  ?uri ?name ?allergy
	# WHERE {
	# 	?uri <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> ?name .
 #  		?uri <http://www.w3.org/2002/07/owl#annotatedTarget> ?allergy 
 #  		FILTER (contains(?allergy, "has_allergic_trigger"))
	# }
	# """

	query = """
		SELECT ?uri ?allergy {
  			?uri <http://www.w3.org/2000/01/rdf-schema#label> ?allergy 
  			FILTER (contains(?allergy, "allergy"))
		}
	"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	synonymResults = {}
	for result in results["results"]["bindings"]:
		synonymResults[result["uri"]["value"]] = result["allergy"]["value"]
	
	return synonymResults


def getDrugAllergy(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	query = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT ?uri ?allergy ?synonym ?allergyType 
		WHERE {
			?uri rdfs:label ?allergy ;
      		rdfs:subClassOf [rdfs:label ?allergyType ] ;
      		<http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> ?synonym
  		FILTER (contains(?allergy, "allergy") && contains(?allergyType, "drug allergy"))
	}
	"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	
	return results["results"]["bindings"]

def getAllergicTrigger(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	medicineAllergy = {}

	query = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		SELECT DISTINCT ?allergy ?allergyType ?medicine
		WHERE {
			?uri rdfs:label ?allergy ;
    		rdfs:subClassOf [rdfs:label ?allergyType ] ;
    		rdfs:subClassOf* [owl:someValuesFrom ?medicine] 
  			FILTER (contains(?allergy, "allergy") && contains(?allergyType, "drug allergy") && ?medicine != ?allergyType)
		}
	"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	resultsAllergicTrigger = sparql.query().convert()["results"]["bindings"]

	queryMedicine = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT ?medicine
		WHERE {
			<%s> rdfs:label ?medicine
		}
		"""

	for result in resultsAllergicTrigger:
		medicine = result['medicine']['value']
		sparql.setQuery(queryMedicine % (medicine))
		sparql.setReturnFormat(JSON)
		resultMedicine = sparql.query().convert()["results"]["bindings"]
		medicineAllergy[result['allergy']['value']] = [r['medicine']['value'] for r in resultMedicine]

	return medicineAllergy

def getAllAllergies(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	allergies = [allergy['allergy']['value'] for allergy in getDrugAllergy()]
	return {'result': list(set(allergies))}

def getAllMedicines(sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	medicines = sum([medicine for medicine in getAllergicTrigger().values()], [])
	return {'result': medicines}

def getMedicineByAllergy(allergyWanted, sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	allergies = getAllergicTrigger()
	return {allergyWanted: allergies[allergyWanted]}

def getAllergyByMedicine(medicineWanted, sparql=SPARQLWrapper("http://localhost:3030/doid/query")):
	result = []
	allergies = getAllergicTrigger()
	for allergy, medicines in allergies.items():
		if medicineWanted in medicines:
			result.append(allergy)
	return {medicineWanted: result}
