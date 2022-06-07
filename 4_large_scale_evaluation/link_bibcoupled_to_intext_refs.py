""" Link references in bibliographic couplings to in-text citation markers.
"""

import json
import os
import re
# import sys

# unarxive_ppr_dir = sys.argv[1]
# fn_links = sys.argv[2]
# fn_out = sys.argv[3]
unarxive_ppr_dir = '/opt/unarXive/unarXive-2020/papers'
# fn_links = 'data/new_connection_refs.json'
fn_links = 'data/new_coupling_refs.json'
num_new_markers = 0
new_citing_papers = set()

with open(fn_links) as f:
    new_conenction_refs = json.load(f)

# iterate over all new connections
new_target_set_links_ext = dict()
for ref_vals in new_conenction_refs:
    fn_paper = os.path.join(
        unarxive_ppr_dir,
        f'{ref_vals["citing_arxiv_id"]}.txt'
    )
    if not os.path.isfile(fn_paper):
        continue
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
    # calc print output stats
    num_new_markers += num_markers
    new_citing_papers.add(ref_vals['citing_arxiv_id'])

print(f'connected {num_new_markers:,} new in-text citation markers')
print(f'in {len(new_citing_papers):,} unique citing papers')
# ## connections
# connected 227,454 new in-text citation markers
# in 8,303 unique citing papers
# ## couplings
# connected 219,630 new in-text citation markers
# in 8,267 unique citing papers
