""" Aggregate reference items
    - newly linked to target collection
    - newly linked through bibliographic coupling
"""

import csv
import json
# import sys

# fn_matching = sys.argv[1]
# fn_contexts = sys.argv[2]
match_threshold = 0.405
fn_matching = 'data/distance_ecbs_t1.json'
fn_contexts = 'data/prepro_expand.csv'

# create a lookup dictionary from reference item CSV line index
# to to reference item values
index_to_ids = dict()
with open(fn_contexts, 'r', encoding='UTF-8') as f:
    csv_reader = csv.DictReader(f)
    for i, row in enumerate(csv_reader):
        index_to_ids[i] = row
print('created lookup dictionary')

# load matching results
with open(fn_matching) as f:
    matching = json.load(f)
print('read matching results')

new_connection_refs = list()  # coupled + added into linked set
new_coupling_refs = list()
new_target_set_links = dict()
# iterate over matching results
print('start processing matches')
for (line_indices, sim) in matching:
    if sim > match_threshold:
        ref_a_vals = index_to_ids[line_indices[0]]
        ref_b_vals = index_to_ids[line_indices[1]]
        if (ref_a_vals['cited_mag_id'] == '' and
           ref_b_vals['cited_mag_id'] == ''):
            # we know nothing from the original data set about this pair
            # -> it's a new bibliographic coupling
            new_coupling_refs.append(ref_a_vals)
            new_coupling_refs.append(ref_b_vals)
            # note newly connected papers
            new_connection_refs.append(ref_a_vals)
            new_connection_refs.append(ref_b_vals)
        elif (ref_a_vals['cited_mag_id'] == '' and
              ref_b_vals['cited_mag_id'] != ''):
            # the original data set had one of the two references linked
            # -> record the new link and the newly connected paper
            # -> a is new
            if ref_b_vals['cited_mag_id'] not in new_target_set_links:
                new_target_set_links[ref_b_vals['cited_mag_id']] = list()
            new_target_set_links[ref_b_vals['cited_mag_id']].append(
                ref_a_vals
            )
            new_connection_refs.append(ref_a_vals)
        elif (ref_a_vals['cited_mag_id'] != '' and
              ref_b_vals['cited_mag_id'] == ''):
            # the original data set had one of the two references linked
            # -> record the new link and the newly connected paper
            # -> b is new
            if ref_a_vals['cited_mag_id'] not in new_target_set_links:
                new_target_set_links[ref_a_vals['cited_mag_id']] = list()
            new_target_set_links[ref_a_vals['cited_mag_id']].append(
                ref_b_vals
            )
            new_connection_refs.append(ref_b_vals)
        else:
            # both cited MAG IDs are set, this means either of
            # the following two cases is true
            # 1. they are identical -> we already knew about the links
            # 2. they are different -> one of the two matchings is wrong
            pass

# process and persist results

print('persisting results')
new_connected_arxiv_ids = set(
    [ref_vals['citing_arxiv_id']
     for ref_vals in new_connection_refs]
)
new_connected_ref_uuids = set(
    [ref_vals['uuid']
     for ref_vals in new_connection_refs]
)
new_coupled_arxiv_ids = set(
    [ref_vals['citing_arxiv_id']
     for ref_vals in new_coupling_refs]
)
new_coupled_ref_uuids = set(
    [ref_vals['uuid']
     for ref_vals in new_coupling_refs]
)
pprs_added_to_citgraph = set()
refs_added_to_citgraph = set()
for cited_mag_id, ref_list in new_target_set_links.items():
    ref_list_arxiv_ids = set(
        [ref_vals['citing_arxiv_id']
         for ref_vals in ref_list]
    )
    pprs_added_to_citgraph = pprs_added_to_citgraph.union(
        ref_list_arxiv_ids
    )
    ref_list_uuids = set(
        [ref_vals['uuid']
         for ref_vals in ref_list]
    )
    refs_added_to_citgraph = refs_added_to_citgraph.union(
        ref_list_uuids
    )
with open('data/new_connection_refs.json', 'w') as f:
    json.dump(new_connection_refs, f)
with open('data/new_coupling_refs.json', 'w') as f:
    json.dump(new_coupling_refs, f)
with open('data/new_target_set_links.json', 'w') as f:
    json.dump(
        {k: list(v) for k, v in new_target_set_links.items()},
        f
    )

print((f'newly connected (=resolved or coupled):\n'
       f'  {len(new_connected_ref_uuids):,} refs in\n'
       f'  {len(new_connected_arxiv_ids):,} unique papers'))
print((f'newly bibliographicly coupled:\n'
       f'  {len(new_coupled_ref_uuids):,} refs in\n'
       f'  {len(new_coupled_arxiv_ids):,} unique papers'))
print((f'added to citation graph:\n'
       f'  {len(refs_added_to_citgraph):,} refs in\n'
       f'  {len(pprs_added_to_citgraph):,} unique papers'))

# newly connected (=resolved or coupled):
#   55,197 refs in
#   8,931 unique papers
# newly bibliographicly coupled:
#   53,940 refs in
#   8,895 unique papers
# added to citation graph:
#   2,442 refs in
#   1,443 unique papers
