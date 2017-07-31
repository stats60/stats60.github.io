"""
generate markdown version of syllabus
"""

import get_syllabus

syll=get_syllabus.get_syllabus()

syll_columns=['Date', 'Topic', 'Reading/Assignment']
header=[i.strip() for i in syll[0]]
syll_colnums=[]
for i,h in enumerate(header):
    if h in syll_columns:
        syll_colnums.append(i)

content=syll[1:]

outfile='syllabus.md'
with open(outfile,'w') as f:
    f.write('| '+'|'.join(syll_columns)+'|\n')
    # create separator
    sep=[]
    for i in range(len(syll_columns)):
        sep.append('---')
    f.write('| '+'|'.join(sep)+'|\n')

    for i,s in enumerate(content):
        rowcontent=[]
        for c in syll_colnums:
            if len(s)>c:
                if s[c].find('no class')>-1:
                    s[c]='**'+s[c]+'**'
                rowcontent.append(s[c])
        f.write('| '+'|'.join(rowcontent)+'|\n')
