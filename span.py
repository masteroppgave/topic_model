#!/usr/bin/python
# coding: utf-8

import json
import shlex
import codecs

"""
Some helper functions to get stats
"""

f = open("superbowltweets.json", "r")
lines = [l for l in f.readlines()]

def isal(string):
	for letter in string:
		if letter.isalpha():
			return True
	return False

def timestamps(lines):
	timestamps = [int(json.loads(line)["timestamp_ms"]) for line in lines]

	return {"max": max(timestamps), "min": min(timestamps)}


def number_of_words(lines):
	total_number_of_words = 0

	for i in xrange(len(lines)):
		text = json.loads(lines[i])["text"].strip()
		total_number_of_words += len(text.split(" "))

	return total_number_of_words

print number_of_words(lines)
