from nef import *
from hrr import *

linestyles=['-','--']
colors=['0.0','0.3','0.6']
linewidths=[2,1]

figsize=(3.5,3)

def color(index):
    return colors[index%len(colors)]
def linestyle(index):
    index=index/2
    return linestyles[index%len(linestyles)]
def linewidth(index):
    return linewidths[index%len(linewidths)]

import numpy
import pylab

D=100
s=HRRNode(D)
vocab=Vocabulary(D,randomize=False)
s.configure(12,saturation_range=(100,200),t_ref=0.002,t_rc=0.02,seed=2,threshold_coverage=0)

ZERO=HRR(data=[0]*D)
steps=20

def get_tuning_curves(node,hrrs,scale=4):
    hrrs=[ZERO]+list(hrrs)+[ZERO]
    x=[]
    for i in range(len(hrrs)-1):
        for j in range(steps+1):
            t=j/float(steps)
            v=hrrs[i].v*(1-t)+hrrs[i+1].v*t
            x.append(v/numpy.sqrt(D)*scale)
    x=numpy.array(x).T

    #x=numpy.array([h.v for h in hrrs]).T
    
    x2=numpy.dot(node.basis,x)
    J=node.alpha*x2.T+node.Jbias
    actv=node.current_to_activity(J.T)

    return actv.T


def analyze(names,letter,labels=None,xticksize=8,markers=[]):
    if labels is None: labels=names
    hrrs=[vocab.parse(x) for x in names]
    a=get_tuning_curves(s,hrrs)
    pylab.figure(figsize=figsize,dpi=300)

    pylab.axes((0.2,0.2,0.75,0.75))
    for i,v in reversed(list(enumerate(a.T))):
        pylab.plot(v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))

    pylab.xticks([(x+1)*steps for x in range(len(hrrs))],labels,rotation=90,fontsize=xticksize,ha='center')
    pylab.xlim(0,len(a))
    pylab.ylabel('firing rate (Hz)')    
    pylab.ylim(0,200)
    pylab.figtext(0.01,0.9,letter,zorder=10,weight='bold')
    for i,(x,y) in enumerate(markers):
        pylab.figtext(x,y,'%d'%(i+1),zorder=10,size=10)
        
    pylab.savefig('fig6%s.png'%letter.lower(),figsize=figsize,dpi=600)

vocab.parse('SQUARE,CIRCLE,TRIANGLE,SHAPE,SIZE,COLOR')

analyze(['SQUARE','CIRCLE','TRIANGLE'],'A',markers=[(0.81,0.56),(0.3,0.29)])
analyze(['SHAPE','COLOR','SIZE'],'B',markers=[(0.6,0.75),(0.81,0.55)])

analyze(['RED*COLOR+CIRCLE*SHAPE','RED*COLOR+TRIANGLE*SHAPE','BLUE*COLOR+TRIANGLE*SHAPE',
         'BLUE*COLOR+SQUARE*SHAPE','GREEN*COLOR+SQUARE*SHAPE','GREEN*COLOR+CIRCLE*SHAPE'],'C',
        labels=['red\ncircle','red\ntriangle','blue\ntriangle','blue\nsquare','green\nsquare','green\ncircle'],xticksize=8,
        markers=[(0.35,0.85),(0.63,0.55)])


pylab.show()

