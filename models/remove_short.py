import json
import os

outy = open("out_1723_may10.json", "a")

with open("1723may_10_2016.json", "r") as f:
	for i, line in enumerate(f):
		l = json.loads(line)

		if len(l["text"]) < 20:
			continue

		#text = "".join([char for char in line["text"] if ord(char) < 128])

		outy.write(line)
