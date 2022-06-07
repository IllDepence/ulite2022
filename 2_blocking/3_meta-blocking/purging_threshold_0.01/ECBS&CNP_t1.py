#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import itertools
import datetime
import math

print(datetime.datetime.now())

with open('result_purgedblock_t1.json') as json_file:  #  try_orderblock1
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
out_edge = open("edges_t1.txt", 'w')  # try_edges
out_edge.writelines(str(edges))
out_edge.close()
'''


def get_number_of_common_blocks(edge):
    global weight
    counter = 0
    counter0 = 0
    counter1 = 0
    entities = list(edge)
    b = len(blocks)
    for block in blocks:
        entities_list = blocks[block]
        if entities[0] in entities_list and entities[1] in entities_list:
            counter += 1
        if entities[0] in entities_list:
            counter0 += 1
        if entities[1] in entities_list:
            counter1 += 1
        try:
            if counter0 != 0 and counter1 != 0:
                weight = counter * math.log10(b / counter0) * math.log10(b / counter1)
                weight = round(weight, 5)
        except ValueError:
            return False
    return weight


def common_block_scheme():
    for edge_index, edge in enumerate(edges):
        edge_weights[edge_index] = get_number_of_common_blocks(edge)
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
    print(float(blocking_cardinality) / float(len(nodes)))
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
    out_directed_edges = open("directed_edges_t1.txt", 'w')  
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
    with open('directed_block_t1.json', 'w') as directed_block_out:
        json.dump(directed_blocks, directed_block_out)
        '''
    return directed_blocks


# Collect the blocks based on the graph from node cardinality pruning.
def collect_graph_blocks():
    result_blocks = []
    for edge in directed_edges:
        if edge is not None:
            result_blocks.append(edge)
    with open('block_ecbs_t1.json', 'w') as result_out:
        json.dump(result_blocks, result_out)
    return result_blocks


def print_number_of_edges_per_node():
    for node in nodes:
        number_of_edges = 0
        for edge in directed_edges:
            if node == list(edge)[0]:
                number_of_edges += 1
            elif node == list(edge)[1]:
                number_of_edges += 1
        print(number_of_edges)


# Weighting scheme
common_block_scheme()

# Pruning scheme
directed_edges = cardinality_node_pruning()

# Collecting the new blocks
directed_result_blocks = collect_directed_graph_blocks(directed_edges)
result_blocks = collect_graph_blocks()

print(datetime.datetime.now())
