""" Link references newly linked to target collection to in-text citation
    markers.
"""

import json
import os
import re
# import sys

# unarxive_ppr_dir = sys.argv[1]
# fn_links = sys.argv[2]
# fn_out = sys.argv[3]
unarxive_ppr_dir = '/opt/unarXive/unarXive-2020/papers'
fn_links = 'new_target_set_links.json'
fn_out = 'new_target_set_links_ext.json'
num_new_markers = 0
new_citing_papers = set()

with open(fn_links) as f:
    new_target_set_links = json.load(f)

# iterate over all new connections
new_target_set_links_ext = dict()
for cited_mag_id, ref_list in new_target_set_links.items():
    if cited_mag_id not in new_target_set_links_ext:
        new_target_set_links_ext[cited_mag_id] = list()
    # get in-text citation marker offsets for all refs
    files_found = 0
    for ref_vals in ref_list:
        ref_vals_ext = ref_vals.copy()
        fn_paper = os.path.join(
            unarxive_ppr_dir,
            f'{ref_vals["citing_arxiv_id"]}.txt'
        )
        if not os.path.isfile(fn_paper):
            ref_vals_ext['plaintext_found'] = False
            ref_vals_ext['number_intext_markers'] = None
            ref_vals_ext['intext_marker_offsets'] = []
            new_target_set_links_ext[cited_mag_id].append(ref_vals_ext)
            continue
        files_found += 1
        # read fulltext
        with open(fn_paper) as f:
            paper_fulltext = f.read()
        # find citation markers
        marker_uuid = ref_vals['uuid']
        cit_marker = '{{cite:' + marker_uuid + '}}'
        matches = re.finditer(
            re.escape(cit_marker),
            paper_fulltext,
            re.M
        )
        # store offsets and total number
        num_markers = 0
        marker_offsets = list()
        for m in matches:
            num_markers += 1
            marker_offsets.append(
                [m.start(), m.end()]
            )
        ref_vals_ext['plaintext_found'] = True
        ref_vals_ext['number_intext_markers'] = num_markers
        ref_vals_ext['intext_marker_offsets'] = marker_offsets
        # calc print output stats
        num_new_markers += num_markers
        new_citing_papers.add(ref_vals['citing_arxiv_id'])
        new_target_set_links_ext[cited_mag_id].append(ref_vals_ext)

with open(fn_out, 'w') as f:
    json.dump(new_target_set_links_ext, f)

print(f'linked {num_new_markers:,} new in-text citation markers')
print(f'in {len(new_citing_papers):,} unique citing papers')
# linked 7,824 new in-text citation markers
# in 1,401 unique citing papers
