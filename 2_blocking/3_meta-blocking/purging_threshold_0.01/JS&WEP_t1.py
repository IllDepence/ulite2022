#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import itertools
import datetime

print(datetime.datetime.now())

with open('result_purgedblock_t1.json') as json_file:
    blocks = json.load(json_file)
nodes = []
edges = []
edge_weights = dict()
i = 0

# graph building
for block in blocks:
    # Add all the entities from the blocks in to 'nodes'
    for entity in blocks[block]:
        if entity not in nodes:
            nodes.append(entity)
    i = i + 1
    # Get all permutations of 2 entities from a block
    permutations = itertools.permutations(blocks[block], 2)
    for permutation in permutations:
        # Create a non-directed edge for each permutation using 'set()'
        edge = {permutation[0], permutation[1]}
        # Add each non-directed edge in to 'edges' once
        if len(edge) == 2 and edge not in edges:
            # this is why we have edges as sets
            edges.append(edge)
'''            
# write edges in txt file
out_edge = open("edges_t1.txt", 'w') 
out_edge.writelines(str(edges))
out_edge.close()
'''


# How many common blocks 2 entities share
def get_number_of_common_blocks(edge):
    counter = 0
    entities = list(edge)
    for block in blocks:
        entities_list = blocks[block]
        if entities[0] in entities_list and entities[1] in entities_list:
            counter += 1
    return counter


# How many blocks is an entity in
def get_number_of_common_blocks_for_entity(entity):
    counter = 0
    for block in blocks:
        entities_list = blocks[block]
        if entity in entities_list:
            counter += 1
    return counter


# Blocking scheme where the edges are weighted based
# on how similar 2 entities are when looking at their blocks
def jaccard_scheme():
    for edge_index, edge in enumerate(edges):
        entities = list(edge)
        number_of_common_blocks = get_number_of_common_blocks(edge)
        num_of_A = get_number_of_common_blocks_for_entity(entities[0])
        num_of_B = get_number_of_common_blocks_for_entity(entities[1])
        weight = float(number_of_common_blocks) / float(num_of_A + num_of_B - number_of_common_blocks)
        edge_weights[edge_index] = round(weight, 5)
    '''
    with open('edge_weights_t1.json', 'w') as edge_weights_out:  # write edge weights in file
        json.dump(edge_weights, edge_weights_out)
    '''


def get_average_edge_weight_of_graph():
    average_weight = 0
    for weight in edge_weights:
        average_weight += edge_weights[weight]
    number_of_weights = float(len(edge_weights))
    average_weight = float(average_weight) / number_of_weights
    '''
    # write average weight and number of edges in file
    with open("stat1.txt", 'w') as out_stat:
        out_stat.write(str(average_weight))
        out_stat.write('\n')
        out_stat.write(str(number_of_weights))
    '''
    return average_weight


# Pruning threshold is the average weight
# if the weight is below average, the edges are removed
def weight_edge_pruning():
    average_weight = get_average_edge_weight_of_graph()
    print(average_weight)
    for edge_index, weight in edge_weights.items():
        if weight < average_weight:
            edges[edge_index] = None


# Collect the blocks based on the graph from weighted edge pruning.
def collect_graph_blocks():
    result_blocks = []
    for edge in edges:
        if edge is not None:
            result_blocks.append(edge)
    with open('block_js_t1.txt', 'w') as file:
        file.write(str(result_blocks))
    return result_blocks


# Weighting schemes
jaccard_scheme()

# Pruning schemes
weight_edge_pruning()

# Collecting the new blocks
resultBlocks = collect_graph_blocks()
'''
with open("stat2.txt", 'w') as out_stat:
    out_stat.write(str(len(resultBlocks)))
'''
