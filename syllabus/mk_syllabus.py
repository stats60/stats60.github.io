"""
generate markdown version of syllabus
"""

import os
import collections
import re
import time
import pandas

from get_syllabus2 import get_syllabus


def replacemany(adict, astring):
    # from https://stackoverflow.com/questions/2392623/replace-multiple-string-in-a-file # noqa
    pat = '|'.join(re.escape(s) for s in adict)
    there = re.compile(pat)
    def onerepl(mo): return adict[mo.group()]
    return there.sub(onerepl, astring)


lecturebase = '../lectures'
if not os.path.exists(lecturebase):
    os.mkdir(lecturebase)

syll = get_syllabus()

df = pandas.DataFrame(syll[1:],columns=syll[0])
df = df.loc[df.Week!='', :]  # remove empty rows

# columns to use for syllabus
syll_columns = ['Date', 'Topic', 'Reading']

# save objectives to write to a separate file listing all of them
objectives = collections.OrderedDict()

outfile = 'index.md'
with open(outfile, 'w') as f:
    f.write('---\nlayout: default\ntitle: Stats 60: Syllabus\n---\n') # noqa
    f.write('## Syllabus\n\nClick on the "Details" line for more information about each lecture\n\n') # noqa
    # f.write('Detailed version of the full syllabus is available [here](../full_syllabus)\n\n') # noqa
    f.write('| '+'|'.join(syll_columns) + '|\n')

    # create separator
    sep = []
    for i in range(len(syll_columns)):
        sep.append('---')
    f.write('| ' + '|'.join(sep) + '|\n')

    # loop through rows
    lecturectr = 1
    for i in df.index:
        df_row = df.loc[i,:]

        if df_row.Topic.lower().find('no class') > -1:
            noclass = True
        else:
            noclass = False

        date = df_row.Date
        topic = '**' + df_row.Topic.replace('\n', '<br>') + '**'
        if df_row.Reading is None:
            reading = ''
        else:
            reading = df_row.Reading.replace('\n', '<br>')

        # create foldout detail

        # add expandable section with learning objectives and links
        details = ''
        if df_row['Learning Objectives'] is not None:
            learnobj = df_row['Learning Objectives'].split('\n')
            if len(learnobj) > 0:
                details += '<details><br>Learning Objectives:<br><br>After this lecture, you should be able to:<br>' # noqa
                groupname = df_row.Topic.split(',')[0]
                if not groupname in objectives:
                    objectives[groupname] = []
                for li, l in enumerate(learnobj):
                    if len(l) == 0:
                        continue
                    objectives[groupname].append(l)
                    details += '* %s<br>' % l
                print(details)

        if df_row['Links'] is not None:
            links = df_row['Links'].split('\n')
            if len(links[0]) > 0:
                details += '<br>Links:<br>'
                for li, l in enumerate(links):
                    details += '* %s<br>' % l
        if details is not '':
            details += '</details><br>'

        if noclass:
            rowcontent =  [df_row.Date, '**' + df_row.Topic + '**', '']
        else:
            rowcontent = [
                df_row.Date,
                '**' + df_row.Topic + '**' + details,
                reading]

        f.write('| ' + '|'.join(rowcontent) + '|\n')

# make a fully expanded version of the syllabus

adict = {'<details>': '<br>', '</details>': ''}

short_syllabus = open('index.md').readlines()
if not os.path.exists('../full_syllabus'):
    os.mkdir('../full_syllabus')

prospectus = open('../prospectus/index.md').readlines()
ssyl = open('index.md').readlines()

with open('../full_syllabus/index.md', 'w') as f:
    f.write('---\nlayout: default\ntitle: Psych 10: Full Syllabus\n---\n') # noqa
    f.write('Revised %s' % time.strftime("%m/%d/%Y"))
    for l in prospectus[4:]:
        f.write(l)
    f.write('## Class Schedule\n')
    for l in short_syllabus[9:]:
        f.write(replacemany(adict, l))

if not os.path.exists("../objectives"):
    os.mkdir('../objectives')
with open('../objectives/index.md', 'w') as f:
    f.write('---\nlayout: default\ntitle: Psych 10: Learning Objectives\n---\n') # noqa
    f.write('## Learning objectives\n\n')
    f.write('Students should be able to do each of the following by the end of this course:\n\n') # noqa

    for k in objectives.keys():
        if len(objectives[k]) == 0:
            continue
        f.write('\n### %s\n' % k)
        for o in objectives[k]:
            f.write('* %s\n' % o)
