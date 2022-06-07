#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import itertools
import datetime
import math

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
    # print(nodes)
    # Get all permutations of 2 entities from a block
    permutations = itertools.permutations(blocks[block], 2)
    # print(permutations)
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
def calculate_common_blocks(edge):
    counter = 0
    entities = list(edge)
    for block in blocks:
        entities_list = blocks[block]
        if entities[0] in entities_list and entities[1] in entities_list:
            common_block = blocks[block]
            size = len(common_block)
            individual_cardinality = size * (size - 1) / 2
            counter = counter + 1 / individual_cardinality
    return round(counter, 5)


# Blocking scheme where the edges are weighted based
# on the sum of the reciprocal individual cardinalities of the common blocks.
def aggregate_reciprocal_comparisons_scheme():
    for edge_index, edge in enumerate(edges):
        edge_weights[edge_index] = calculate_common_blocks(edge)
    '''   
    out_edge_weight = open("edges_weight_t1.txt", 'w')
    out_edge_weight.writelines(str(edge_weights))
    out_edge_weight.close()
'''


def get_weighted_neighborhood(node):
    # creating a list of the neighboring edges with tuples of the edge index in the main edge list and its weight
    neighbor_edges_indices = []
    for index, edge in enumerate(edges):
        if node == list(edge)[0]:
            neighbor_edges_indices.append((index, edge_weights[index]))
        elif node == list(edge)[1]:
            neighbor_edges_indices.append((index, edge_weights[index]))
    return neighbor_edges_indices


def calculate_blocking_cardinality():
    blocking_cardinality = 0
    for block in blocks:
        blocking_cardinality += len(blocks[block])
    return float(blocking_cardinality) / float(len(nodes))


def calculate_k(blocking_cardinality):
    return int(math.floor(blocking_cardinality-1))


def calculate_local_k(neighborhood):
    cardinality_of_edges = len(neighborhood)
    k = int(math.ceil(0.1 * cardinality_of_edges))
    return k


def cardinality_node_pruning():
    directed_edges = []
    for node in nodes:
        # getting all neighboring edges and their weights
        neighbor_edge_index_and_weights = get_weighted_neighborhood(node)
        # get k
        k = calculate_local_k(neighbor_edge_index_and_weights)
        # sorting the neighboring edges by their weight
        neighbor_edge_index_and_weights = sorted(neighbor_edge_index_and_weights,
                                                 key=lambda weight: weight[1], reverse=True)
        # selecting the top k edges
        top_k_edge_index_and_weights = neighbor_edge_index_and_weights[:k]
        # creating a directed edge for every top k edge
        for edge_index_and_weight in top_k_edge_index_and_weights:
            # from the original edges list, take the top k indices we just computed
            original_edge = list(edges[edge_index_and_weight[0]])
            # checking if the root of the edge is the node we are analysing
            if original_edge[0] == node:
                directed_edges.append(original_edge)
            else:
                original_edge.reverse()
                directed_edges.append(original_edge)
    '''
    out_directed_edges = open("directed_edges_t1.txt", 'w')  # try_directed_edges
    out_directed_edges.writelines(str(directed_edges))
    out_directed_edges.close()
    '''
    return directed_edges


# Collect the new blocks based on the graph from cardinality node pruning.
# A block is created by taking a nodes directed edges
# and combining the nodes that are pointed at it to a block.
def collect_directed_graph_blocks(directed_edges):
    directed_blocks = dict()
    for edge in directed_edges:
        # if the origin node of the arrow already has a block
        if edge[0] in directed_blocks:
            directed_blocks[edge[0]].append(edge[1])
    # create a new block for the edges origin node
        else:
            directed_blocks[edge[0]] = [edge[1]]
    '''  
    with open('directed_block_t1.json', 'w') as directed_block_out:  # try_directed_block
        json.dump(directed_blocks, directed_block_out)
    '''
    return directed_blocks


# Collect the blocks based on the graph from node cardinality pruning.
def collect_graph_blocks():
    result_blocks = []
    for edge in directed_edges:
        if edge is not None:
            result_blocks.append(edge)
    with open('block_arcscnp_t1.json', 'w') as result_out:
        json.dump(result_blocks, result_out)
    return result_blocks


# Weighting scheme
aggregate_reciprocal_comparisons_scheme()
# Pruning scheme
directed_edges = cardinality_node_pruning()

# Collecting the new blocks
directed_result_blocks = collect_directed_graph_blocks(directed_edges)
result_blocks = collect_graph_blocks()
'''
with open("stat2_t1.txt", 'w') as out_stat:
    out_stat.write(str(len(result_blocks)))
'''
