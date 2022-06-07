#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re

# expand abbreviation of journal and conference name to full name
with open('abbrev_proc.csv') as abbrev_p:
    abbrev_proc = dict(map(str.strip, line.partition(',')[::2])  for line in abbrev_p if line.strip())
    abbrev_proc_sorted = sorted(abbrev_proc, key=len, reverse=True)
with open('abbrev_journal.csv') as abbrev_j:
    abbrev_journal = dict(map(str.strip, line.partition(',')[::2])  for line in abbrev_j if line.strip())
    abbrev_journ_sorted = sorted(abbrev_journal, key=len, reverse=True)
with open("prepro_result.csv", "r", encoding='UTF-8') as csvin:
    reader = csv.DictReader(csvin)
    with open("prepro_expand.csv", 'w', newline='', encoding="utf-8") as csvout:
        writer = csv.DictWriter(csvout, fieldnames=['uuid', 'citing_mag_id', 'cited_mag_id', 'citing_arxiv_id',
                                                    'cited_arxiv_id', 'bibitem_string', 'parsed_string', 'entry_type',
                                                    'author', 'title', 'booktitle', 'journal', 'year', 'pages',
                                                    'volume', 'journal_new', 'booktitle_new'])
        writer.writeheader()
        for row in reader:
            value_bt = row['booktitle']
            value_j = row['journal']
            regex_bt = re.findall(r"\b({})\b".format("|".join(map(re.escape, abbrev_proc_sorted))), value_bt)
            regex_j = re.findall(r"\b({})\b".format("|".join(map(re.escape, abbrev_journ_sorted))), value_j)
            if len(value_bt) != 0:
                if len(regex_bt) != 0:
                    for key in regex_bt:
                        row['booktitle_new'] = abbrev_proc[key]
                        break
                else:
                    row['booktitle_new'] = value_bt

            else:
                row['booktitle_new'] = ''
            if len(value_j) != 0:
                if len(regex_j) != 0:
                    for key in regex_j:
                        row['journal_new'] = abbrev_journal[key]
                        break
                else:
                    row['journal_new'] = value_j
            else:
                row['journal_new'] = ''
            writer.writerow(row)
