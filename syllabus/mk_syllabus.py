"""
generate markdown version of syllabus
"""

import os,collections

import get_syllabus

lecturebase='../lectures'
if not os.path.exists(lecturebase):
    os.mkdir(lecturebase)

syll=get_syllabus.get_syllabus()

syll_columns=['Date', 'Topic', 'Reading']
header=[i.strip() for i in syll[0]]
syll_colnums=[]
header_index={}
for i,h in enumerate(header):
    if h in syll_columns:
        syll_colnums.append(i)
    header_index[h]=i


content=syll[1:]

# save objectives to write to a separate file listing all of them
objectives=collections.OrderedDict()

outfile='index.md'
with open(outfile,'w') as f:
    f.write('---\nlayout: default\ntitle: Psych 10: Syllabus\n---\n')
    f.write('## Syllabus\n\nClick on the date for more information about each lecture\n\n')
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
                rowcontent.append(s[c].replace('\n','<br>'))
        if s[0]=='TBD':
            noclass=True
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
                lf.write('# Lecture %d (%s): %s\n\n'%(lecturectr,
                            s[0],s[1]))
                if len(s)>header_index['Learning Objectives']:
                    lf.write('### Learning Objectives:\nAfter this lecture, you should be able to:\n')
                    learnobj=s[header_index['Learning Objectives']].split('\n')
                    groupname=s[1].split(',')[0]
                    if not s[1] in objectives:
                        objectives[groupname]=[]
                    for li,l in enumerate(learnobj):
                        if len(l)==0:
                            continue
                        # lsp=l.split(' ')
                        # l=lsp[1:]
                        # l.append('(%s)'%lsp[0].replace('.',''))
                        # l=' '.join(l)
                        lf.write('* %s\n'%l)
                        objectives[groupname].append(l)
                if len(s)>header_index['Links']:
                    lf.write('\n### Links:\n')
                    links=s[header_index['Links']].split('\n')
                    for li,l in enumerate(links):
                        lf.write('* %s\n'%l)
            lecturectr+=1

if not os.path.exists("../objectives"):
    os.mkdir('../objectives')
with open('../objectives/index.md','w') as f:
    f.write('---\nlayout: default\ntitle: Psych 10: Learning Objectives\n---\n')
    f.write('## Learning objectives\n\n')
    f.write('Students should be able to do each of the following by the end of this course:\n\n')

    for k in objectives.keys():
        if len(objectives[k])==0:
            continue
        f.write('\n### %s\n'%k)
        for o in objectives[k]:
            f.write('* %s\n'%o)
