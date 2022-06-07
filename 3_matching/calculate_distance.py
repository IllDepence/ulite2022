#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import csv
import datetime


def jaccard_similarity(row0, row1):
    list1 = row0.split()
    list2 = row1.split()
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union


result = []
output = []
with open('prepro_expand.csv', "r", encoding='UTF-8') as data:
    reader = csv.DictReader(data)
    rows = [row for row in reader]
    # change different blocking results to calculate distance for different configurations
    with open('block_cbs_t1.json') as json_file:
        blocks = json.load(json_file)
        for block in blocks:
            i = 0
            for row in rows:
                if i == block[0]:
                    row_0 = row
                if i == block[1]:
                    row_1 = row
                i = i + 1
            if len(row_0['title']) != 0 and len(row_1['title']) != 0:
                title_dis = jaccard_similarity(row_0['title'], row_1['title'])
            else:
                title_dis = 0

            if len(row_0['author']) != 0 and len(row_1['author']) != 0:
                author_dis = jaccard_similarity(row_0['author'], row_1['author'])
            else:
                author_dis = 0

            if len(row_0['booktitle_new']) != 0 and len(row_1['booktitle_new']) != 0:
                booktitle_dis = jaccard_similarity(row_0['booktitle_new'], row_1['booktitle_new'])
            else:
                booktitle_dis = 0

            if len(row_0['journal_new']) != 0 and len(row_1['journal_new']) != 0:
                journal_dis = jaccard_similarity(row_0['journal_new'], row_1['journal_new'])
            else:
                journal_dis = 0

            if len(row_0['volume']) != 0 and len(row_1['volume']) != 0:
                volume_dis = jaccard_similarity(row_0['volume'], row_1['volume'])
            else:
                volume_dis = 0

            if len(row_0['year']) != 0 and len(row_1['year']) != 0:
                year_dis = jaccard_similarity(row_0['year'], row_1['year'])
            else:
                year_dis = 0

            if len(row_0['pages']) != 0 and len(row_1['pages']) != 0:
                pages_dis = jaccard_similarity(row_0['pages'], row_1['pages'])
            else:
                pages_dis = 0
            total_dis = 8*title_dis + 6*author_dis + 5*booktitle_dis + 5*journal_dis \
                        + 2*volume_dis + 3*year_dis + 2*pages_dis
            result1 = [block, round(1/31 * total_dis, 5)]
            result.append(result1)
            print(round(1/31 * total_dis, 5))
        out_result = open("distance_cbs_t1.txt", 'w')
        out_result.writelines(str(result))
        out_result.close()




