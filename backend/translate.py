#/* Copyright (C) Florentina Petcu - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Florentina Petcu <florentina.ptc@gmail.com>, December 2018
# */

from googletrans import Translator


def translateSynonym(synonym):
	translator = Translator()
	return translator.translate(synonym, dest='ro').text