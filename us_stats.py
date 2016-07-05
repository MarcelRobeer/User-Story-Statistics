#!/usr/bin/env python

import csv
import pandas
from spacy.en import English

from rules import *

#####################
# Helper methods
def add(matrix, index, column, by=1):
		return matrix.set_value(index, column, matrix.at[index,column]+by)
		
#####################
# Declarations
storysets = []
stories = []

nlp = English()

#####################
# Read file
csvfile = open("STORIES.csv")
reader = csv.reader(csvfile, delimiter=',', quotechar='"')


#####################
# Get all numbers of story sets and parse the stories
#####################
# row[0]: set ID
# row[1]: user story
for row in reader:
	storysets.append(row[0])
	stories.append([row[0], nlp(row[1]), row[1]])


#####################
# Remove duplicate number of story sets and sort
storysets = list(set(storysets))
storysets.sort(key=int)


#####################
# Create the column names
general_columns = ["N"]
rules = ["C1", "C2", "C3", "C4", "C5", "R1", "R2", "R3", "R4", "R5", "R6", "H1", "H2", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "CA1", "CA2", "CA3", "CA4"]
cols = general_columns + rules


#####################
# Create the stats dataframe
stats = pandas.DataFrame(0, index=storysets, columns=cols)


#####################
# story[0]: number of story set story originated from
# story[1]: tokenized story
# story[2]: original story
#####################

#####################
# Test rules
for story in stories:
	stats = add(stats, story[0], "N")
	for rule in rules:
		if eval("Rules." + rule + "(story[1])"):
			stats = add(stats, story[0], rule)

#####################
# Show in console
print(stats)

#####################
# Print to csv
stats.to_csv(path_or_buf="story_stats.csv", sep=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
