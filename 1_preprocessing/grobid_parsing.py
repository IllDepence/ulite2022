#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import re
import requests

i = 0
with open('unarXive-2020-bibitem.csv', "r", encoding='UTF-8') as data:
    reader = csv.DictReader(data)
    with open('parsed_result.csv', 'w', newline='', encoding='UTF-8') as wf:
        writer = csv.DictWriter(wf, fieldnames=['uuid','citing_mag_id','cited_mag_id','citing_arxiv_id','cited_arxiv_id','bibitem_string','parsed_string'])
        writer.writeheader()
        for row in reader:
            value_ref = row['bibitem_string'].encode('utf-8')
            value_str = str(value_ref, encoding="utf-8")
            value_clean = re.sub('¦', '', value_str)
            value_input = {'citations': value_clean}

            url = "http://localhost:8070/api/processCitation"
            headers = {'Accept': 'application/x-bibtex', 'Content-Type': 'application/x-www-form-urlencoded'}
            if len(value_ref) != 0:
                resp = requests.post(url, headers=headers, data=value_input)
                row['parsed_string'] = resp.text
            else:
                row['parsed_string'] = ''
            writer.writerow(row)
            i = i + 1
            if i % 10000 == 0:
                print(i)