"""
generate markdown version of syllabus
"""

import os
import get_syllabus

lecturebase='../lectures'
if not os.path.exists(lecturebase):
    os.mkdir(lecturebase)

syll=get_syllabus.get_syllabus()

syll_columns=['Date', 'Topic', 'Reading/Assignment']
header=[i.strip() for i in syll[0]]
syll_colnums=[]
for i,h in enumerate(header):
    if h in syll_columns:
        syll_colnums.append(i)

content=syll[1:]

outfile='index.md'
with open(outfile,'w') as f:
    f.write('---\nlayout: default\ntitle: Psych 10: Syllabus\n---\n')
    f.write('| '+'|'.join(syll_columns)+'|\n')
    # create separator
    sep=[]
    for i in range(len(syll_columns)):
        sep.append('---')
    f.write('| '+'|'.join(sep)+'|\n')
    lecturectr=1
    for i,s in enumerate(content):
        rowcontent=[]
        noclass=False
        for c in syll_colnums:
            if len(s)>c:
                if s[c].find('no class')>-1:
                    s[c]='**'+s[c]+'**'
                    noclass=True
                rowcontent.append(s[c])
        if not noclass:
            # add link
            rowcontent[0]='[%s](../lectures/lecture%02d)'%(rowcontent[0],lecturectr)
        f.write('| '+'|'.join(rowcontent)+'|\n')
        if not noclass:
            # create lecture dir and link
            lecturenum='lecture%02d'%lecturectr
            lecturedir=os.path.join(lecturebase,lecturenum)
            if not os.path.exists(lecturedir):
                os.mkdir(lecturedir)
            lecturefile=os.path.join(lecturedir,'index.md')
            with open(lecturefile,'w') as lf:
                lf.write('---\nlayout: default\ntitle: Psych 10: Lecture %d\n---\n'%lecturectr)
                lf.write('# Lecture %d (%s): %s\n\n### Learning Objectives:\n'%(lecturectr,
                            s[0],s[1]))
                if len(s)>6:
                    learnobj=s[6].split('\n')
                    for li,l in enumerate(learnobj):
                        if len(l)==0:
                            continue
                        lsp=l.split(' ')
                        l=lsp[1:]
                        l.append('(%s)'%lsp[0].replace('.',''))
                        l=' '.join(l)
                        lf.write('%d. %s\n'%(li+1,l))
            lecturectr+=1
