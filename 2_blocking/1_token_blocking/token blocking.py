#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re
import json
from itertools import islice

blocks = dict()


# create a block for each distinct token
def token_blocking():
	index = 0
	with open("prepro_expand.csv", "r", encoding='UTF-8') as data:
		reader = csv.reader(data)
		for row in islice(reader, 1, None):
			lines = row[8] + ' ' + row[9] + ' ' + row[15] + ' ' + row[16] + ' ' + row[12] + ' ' + row[13] + ' ' + row[14]
			line = re.sub('\s+', ' ', lines)
			for word in line.split():
				if word in blocks:
					if set([index]) < set(blocks[word]):   # value of key in the list, skip
						continue
					else:
						blocks[word].append(index)  # not duplicate,then add
				else:
					blocks[word] = [index]
			index += 1
	with open('result_block.json', 'w') as outfile:
		json.dump(blocks, outfile)
	return blocks


order_block = dict()


# order blocks according to the size
def block_order():
	for k in sorted(blocks, key=lambda k: len(blocks[k])):
		order_block[k] = blocks[k]
	with open('result_orderblock.json', 'w') as orderedblock:
		json.dump(order_block, orderedblock)
	return order_block


token_blocking()
block_order()






