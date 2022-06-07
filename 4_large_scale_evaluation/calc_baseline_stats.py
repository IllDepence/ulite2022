""" Calculate basic stats for papers, reference items, and in-text citations
    already linked to the target collection.
"""

import csv
import os
import re
import numpy as np
# import sys

# unarxive_ppr_dir = sys.argv[1]
# fn_refs = sys.argv[2]
# fn_disciplines = sys.argv[3]
unarxive_ppr_dir = '/opt/unarXive/unarXive-2020/papers'
fn_refs = 'data/prepro_expand.csv'
fn_disciplines = 'data/citing_ppr_disciplines.csv'

old_connected_arxiv_ids = set()
num_old_reflinks = 0
num_old_markers = 0
cited_years = list()
with open(fn_refs, 'r', encoding='UTF-8') as f:
    csv_reader = csv.DictReader(f)
    for ref_vals in csv_reader:
        # get cited year
        bibtext_str = ref_vals['parsed_string']
        year_match = re.search(r'year = \{(\d\d\d\d)\}', bibtext_str)
        if year_match is None:
            year = -1
        else:
            year = int(year_match.group(1))
        if year > 1700 and year < 2021:
            cited_years.append(int(ref_vals['year']))
        # get stats on linked refs
        if ref_vals['cited_mag_id'] == '':
            continue
        num_old_reflinks += 1
        old_connected_arxiv_ids.add(ref_vals['citing_arxiv_id'])
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
        num_old_markers += num_markers

with open(fn_disciplines, 'r', encoding='UTF-8') as f:
    csv_reader = csv.DictReader(f)
    seen_arxiv_ids = list()
    discipline_counts = dict()
    for row in csv_reader:
        if row['arxiv_id'] in seen_arxiv_ids:
            # only take the first (=main)
            continue
        seen_arxiv_ids.append(row['arxiv_id'])
        disc = row['discipline'].split(':')[0]
        if disc not in discipline_counts:
            discipline_counts[disc] = 0
        discipline_counts[disc] += 1

print(f'#existing "linked" papers: {len(old_connected_arxiv_ids):,}')
print(f'#existing reflinks: {num_old_reflinks:,}')
print(f'#existing markers: {num_old_markers:,}')
print(f'Cited papers from: {min(cited_years)} – {max(cited_years)}')
print(f'                   (mean {np.mean(cited_years)})')
print(f'                   (median {np.median(cited_years)})')
disc_count_sum = sum(list(discipline_counts.values()))
for discipline, count in discipline_counts.items():
    print((f'{count:,} ({(count/disc_count_sum)*100:.2f}%) '
           f'citing pprs from {discipline}'))
# #existing "linked" papers: 1,590
# #existing reflinks: 13,975
# #existing markers: 23,707
# Cited papers from: 1743 – 2020
#                    (mean 1996.2564547275786)
#                    (median 1999.0)
# 7,347 (74.08%) citing pprs from physics
# 1,686 (17.00%) citing pprs from math
# 789 (7.96%) citing pprs from cs
# 39 (0.39%) citing pprs from q-bio
# 21 (0.21%) citing pprs from stat
# 21 (0.21%) citing pprs from eess
# 10 (0.10%) citing pprs from q-fin
# 4 (0.04%) citing pprs from econ
