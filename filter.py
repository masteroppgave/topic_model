import json, random
from random import shuffle

out = open("_12bad.json", "a")

lines = [line for line in open("bad.json").readlines()]

lines = lines[:12307]

for line in lines:
	out.write(line)
