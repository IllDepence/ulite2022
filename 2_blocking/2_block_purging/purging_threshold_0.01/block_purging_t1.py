#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


with open('result_orderblock.json') as json_file:
    order_block = json.load(json_file)

stat = dict()
newBlocks = dict()
optimal_size = 2
temp = []
tp = []


def block_purging():
    block_assignment = 0
    i = 0
    comparison = 0
    global optimal_size
    for b in order_block:
        size = len(order_block[b])
        if 2 <= size:
            block_assignment = block_assignment + size
            comparison = comparison + size * (size - 1) / 2
            comparison_cardinality = block_assignment / comparison
            stat[size] = [i, size, round(comparison_cardinality, 5)]
        i = i + 1
    for j in sorted(stat, key=lambda j: stat[j]):
        temp.append(stat[j][2])
        tp.append(stat[j][1])

    for k in range(0, len(temp) - 1):
        c = round(temp[k] - temp[k + 1], 5)  #  c: calculate the difference between two adjacent cc
        print(c)
        if c < 0.01:  # if the value of c is smaller than a specific value, then the optimal size is found
            optimal_size = tp[k]
            break
    print(optimal_size)

    for block in order_block:
        if len(order_block[block]) <= optimal_size:
            if len(order_block[block]) >= 2:
                newBlocks[block] = order_block[block]
            else:
                continue
        else:
            continue
    with open('result_purgedblock_t1.json', 'w') as purged_block:
        json.dump(newBlocks, purged_block)
    return newBlocks


block_purging()
