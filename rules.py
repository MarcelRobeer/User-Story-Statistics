import re

class Rules:
	'''
	pos_ refers to the Universal POS Set 
		(https://universaldependencies.github.io/docs/u/pos/)

	tag_ refers to the Penn Treebank POS Set
		(https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)

	dep_ refers to Clear Style dependencies 
		(http://www.mathcs.emory.edu/~choi/doc/clear-dependency-2012.pdf)
	'''

	#########################################
	### CONCEPTS (ENTITY TYPES)             #
	#########################################

	# Every noun is a potential concept
	def C1(story):
		for token in story:
			if token.pos_ == "NOUN":
				return True
		return False

	# Every common noun is a concept
	def C2(story):
		for token in story:
			# In the Penn Treebank POS Tagset, there are no such things as common nouns, but a common noun is the opposite of a proper noun
			if token.pos_ == "NOUN" and (token.tag_ != "NNP" or token.tag_ != "NNPS"):
				return True
		return False

	# The subject of a sentence is a concept
	def C3(story):
		for token in story:
			if token.dep_ == "nsubj":
				return True
		return False

	# Compound nouns are taken together to form a composite concept
	def C4(story):
		for token in story:
			if token.dep_ == "compound":
				return True
		return False		
		
	# A gerund is a concept
	def C5(story):
		for token in story:
			# If gerund or present participle
			if token.tag_ == "VBG":
				# It is a gerund if the previous word is a preposition
				if token.nbor(-1).dep_ == "prep":
					return True
				# It is a gerund if it is part of a noun phrase
				for chunk in story.noun_chunks:
					if token in chunk:
						return True
		return False

	#########################################
	### RELATIONSHIPS			            #
	#########################################

	# A verb indicates a potential relationship
	def R1(story):
		for token in story:
			if token.pos_ == "VERB":
				return True
		return False
	
	# A transitive verb signals a relationship
	# A transitive verb is a verb that is followed by a direct object
	def R2(story):
		for token in story:
			if token.dep_ == "dobj" and token.head.pos_ == "VERB":
				return True
		return False

	# Subject - verb phrase - object form a relationship
	def R3(story):
		# If the sentence has a subject
		if Rules.C3(story):
			for token in story:
				if token.dep_[-3:] == "obj" and token.head.pos_ == "VERB":
					return True
		return False

	# A noun followed by a preposition signifies a relationship
	def R4(story):
		for token in story:
			# If token is a noun and not the last word of the sentence
			if token.dep_ == 'poss' and token.head.pos_ == "NOUN":
				return True
		return False

	# 'The R of X is Y' / 'X is the R of Y' -> relationship
	def R5(story):
		text_story = ' '.join([str.lower(t.text) for t in story])
		m1 = re.match('the (.*?) of (.*?) is (.*?)', text_story)
		m2 = re.match('(.*?) is the (.*?) of (.*?)', text_story)
		if m1 is not None or m2 is not None:
			return True
		return False

	# If there is a compound noun, we form a non-hierarchical relationship between the prefix and the compound
	def R6(story):
		for token in story:
			if token.dep_ == "compound":
				return True
		return False

	#########################################
	### HIERARCHICAL RELATIONSHIPS		    #
	#########################################

	# The presence of the verb 'to be' indicates a hierarchical relationship
	def H1(story):
		for token in story:
			if token.pos_ == "VERB" and str.lower(token.lemma_) == "be":
				return True
		return False

	#
	def H2(story):
		if Rules.C5(story):
			return True
		return False

	#########################################
	### ATTRIBUTES				            #
	#########################################

	# Adjectives are the attribute of the noun phrase main
	def A1(story):
		for chunk in story.noun_chunks:
			for token in chunk:
				if token.pos_ == "ADJ":
					return True
		return False

	# An adverb corresponds to an attribute of an entity
	def A2(story):
		for token in story:
			if token.pos_ == "ADV":
				return True
		return False

	# A possessive apostrophe signifies attribute
	def A3(story):
		for token in story:
			if (token.text == "'" or token.text == "'s") and token.dep_ == 'case':
				return True
		return False

	# The genitive case indicates an attribute
	def A4(story):
		for token in story:
			if token.dep_[-4:] == "poss":
				return True
		return False

	# The verb 'have' indicates an attribute
	def A5(story):
		for token in story:
			if token.pos_ == "VERB" and str.lower(token.lemma_) == "have":
				return True
		return False

	# A word in the set S={'number','no','code','date','type','volume','birth','id','address','name'} may indicate an attribute
	def A6(story):
		indicators = ['number','no','code','date','type','volume','birth','id','address','name']
		for token in story:
			if str.lower(token.lemma_) in indicators:
				return True
		return False

	# Objects of numeric/algebraic operations are attributes
	def A7(story):
		for token in story:
			if token.tag_ == "CD" or token.tag_ == "SYM":
				return True
		return False

	#########################################
	### CARDINALITIES			            #
	#########################################

	# Singular noun -> Exactly 1
	def CA1(story):
		for token in story:
			if token.tag_ == 'NN' or token.tag_ == 'NNP':
				return True
		return False
		
	# More than X -> X..n
	def CA2(story):
		text_story = ' '.join([str.lower(t.text) for t in story])
		if re.match('more than (.*?)', text_story) is not None:
			return True
		return False

	# The words Many/each/all/every/some/any -> ??..n
	def CA3(story):
		signals = ['many', 'each', 'all', 'every', 'some', 'any']
		for token in story:
			if str.lower(token.text) in signals:
				return True
		return False

	# Indefinite article -> Exactly 1
	def CA4(story):
		signals = ['a', 'an']
		for token in story:
			# If indefinite article AND it is not part of the role indicator 'as a'/'as an'
			if str.lower(token.text) in signals:
				if str.lower(token.nbor(-1).text) != 'as':
					return True
		return False
