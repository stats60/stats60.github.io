"""
generate markdown version of syllabus
"""

import os,collections,re

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
        if s[header_index['Topic']].find('no class')>-1 or s[0]=='TBD':
            noclass=True
        else:
            noclass=False

        for c in syll_colnums:
            if not len(s)>c:
                print('skipping',s)
                continue
            if syll_columns[c]=='Topic' and not noclass:
                cellcontent='<details><summary><h4>%s<h4></summary>'%s[c].replace('\n','<br>')
                # add expandable section with details
                if len(s)>header_index['Learning Objectives']:
                    learnobj=s[header_index['Learning Objectives']].split('\n')
                    if len(learnobj)>0:
                        cellcontent+='<h5>Learning Objectives:</h5>After this lecture, you should be able to:<p><ul>'
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
                            #lf.write('* %s\n'%l)
                            objectives[groupname].append(l)
                            cellcontent+='<li>%s</li>'%l
                        cellcontent+='</ul>'
                if len(s)>header_index['Links']:
                    cellcontent+='<h5>Links:</h5>'
                    links=s[header_index['Links']].split('\n')
                    if len(links)>0:
                        cellcontent+='<ul>'
                        for li,l in enumerate(links):
                            cellcontent+='<li>%s</li>'%l
                        cellcontent+='</ul>'
                cellcontent+='</display>'
            else:
                cellcontent=s[c].replace('\n','<br>')
            if noclass:
                cellcontent='**'+cellcontent+'**'
            rowcontent.append(cellcontent)
        print(rowcontent)
        #if not noclass:
            # add link
        #    rowcontent[0]='[%s](../lectures/lecture%02d)'%(rowcontent[0],lecturectr)
        f.write('| '+'|'.join(rowcontent)+'|\n')

# make a fully expanded version of the syllabus

# from https://stackoverflow.com/questions/2392623/replace-multiple-string-in-a-file
def replacemany(adict, astring):
  pat = '|'.join(re.escape(s) for s in adict)
  there = re.compile(pat)
  def onerepl(mo): return adict[mo.group()]
  return there.sub(onerepl, astring)

adict={'<details><summary>':'','</summary>':'','</display>':''}

short_syllabus=open('index.md').readlines()
if not os.path.exists('../full_syllabus'):
    os.mkdir('../full_syllabus')

with open('../full_syllabus/index.md','w') as f:
    for l in short_syllabus:
        f.write(replacemany(adict,l))

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
