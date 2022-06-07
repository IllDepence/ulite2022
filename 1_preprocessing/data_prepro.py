#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re
import unicodedata

# extract every metadata field and normalize separately
with open('parsed_result.csv', "r", encoding='UTF-8') as data:
    reader = csv.DictReader(data)
    with open('prepro_result.csv', 'w', newline='', encoding='UTF-8') as wf:
        writer = csv.DictWriter(wf, fieldnames=['uuid', 'citing_mag_id', 'cited_mag_id', 'citing_arxiv_id',
                                                'cited_arxiv_id', 'bibitem_string', 'parsed_string', 'entry_type',
                                                'author', 'title', 'booktitle', 'journal', 'year', 'pages', 'volume'])
        writer.writeheader()
        for row in reader:
            parsed_string = row['parsed_string']
            if len(parsed_string) != 0:
                p0 = re.compile(r'@.*?{', re.S)
                entry_type = re.findall(p0, parsed_string)

                p1 = re.compile(r'author = {.*?}', re.S)
                parsed_author = re.findall(p1, parsed_string)

                p2 = re.compile(r'[\s\S] title = {.*?}', re.S)
                parsed_title = re.findall(p2, parsed_string)

                p3 = re.compile(r'[\s\S] booktitle = {.*?}', re.S)
                parsed_booktitle = re.findall(p3, parsed_string)

                p4 = re.compile(r'journal = {.*?}', re.S)
                parsed_journal = re.findall(p4, parsed_string)

                p5 = re.compile(r'year = {.*?}', re.S)
                parsed_year1 = re.findall(p5, parsed_string)
                p5_0 = re.compile(r'\d+', re.S)  # remove other characters, only digits are left
                parsed_year = re.findall(p5_0, ''.join(parsed_year1))

                p6 = re.compile(r'pages = {.*?}', re.S)
                parsed_pages = re.findall(p6, parsed_string)
                p7 = re.compile(r'volume = {.*?}', re.S)
                parsed_volume = re.findall(p7, parsed_string)

                row['entry_type'] = ''.join(entry_type)[1:-1]

                author_0 = ''.join(parsed_author)[10:-1].lower()
                author_1 = re.sub('[0-9]', '', author_0)
                author_1 = re.sub('\W+', ' ', author_1)
                author_1 = re.sub('\s+', ' ', author_1)
                # the following three steps aim at facilitating token-blocking
                author_1 = re.sub(' and ', ';', author_1)
                author_1 = re.sub(' ', '-', author_1)
                author_1 = re.sub(';', ' ', author_1)
                author = unicodedata.normalize('NFKD', author_1).encode('ascii', 'ignore')
                row['author'] = author.decode('UTF-8')

                title_0 = ''.join(parsed_title)[11:-1].lower()
                title_1 = re.sub('\W+', ' ', title_0)  # remove other characters
                title_1 = re.sub('\s+', ' ', title_1)
                title = unicodedata.normalize('NFKD', title_1).encode('ascii', 'ignore')
                row['title'] = title.decode('UTF-8')

                BookTitle_0 = ''.join(parsed_booktitle)[15:-1].lower()
                BookTitle_1 = re.sub('\W+', ' ', BookTitle_0)
                BookTitle_1 = re.sub('\s+', ' ', BookTitle_1)
                BookTitle = unicodedata.normalize('NFKD', BookTitle_1).encode('ascii', 'ignore')
                row['booktitle'] = BookTitle.decode('UTF-8')

                journal_0 = ''.join(parsed_journal)[11:-1].lower()
                journal_1 = re.sub('\W+', ' ', journal_0)
                journal_1 = re.sub('\s+', ' ', journal_1)
                journal = unicodedata.normalize('NFKD', journal_1).encode('ascii', 'ignore')
                row['journal'] = journal.decode('UTF-8')

                row['year'] = ''.join(parsed_year)[0:4]

                pages_0 = ''.join(parsed_pages)[9:-1]
                row['pages'] = re.sub('--', ' ', pages_0)

                row['volume'] = ''.join(parsed_volume)[10:-1]
                row['parsed_string'] = re.sub('\n', ' ', parsed_string)
            writer.writerow(row)
