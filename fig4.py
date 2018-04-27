from nef import *

linestyles=['-','--']
colors=['0.0','0.3','0.6']
linewidths=[1,2]

figsize=(3.5,3)

def color(index):
    return colors[index%len(colors)]
def linestyle(index):
    index=index/2
    return linestyles[index%len(linestyles)]
def linewidth(index):
    return linewidths[index%len(linewidths)]

s=ScalarNode()
s.configure(12,saturation_range=(100,200),t_ref=0.002,t_rc=0.02,threshold_coverage=0.7,seed=3)
import numpy
def get_tuning_curves(node,dx=0.005,apply_sign=False,scale=1):
    x=numpy.arange(node.min,node.max,dx)
    alpha=node.alpha
    if apply_sign:
        sign=numpy.sign(node.basis[:,0])
        sign.shape=sign.shape[0]
        alpha=alpha*sign
            
    J=numpy.outer(alpha,x).T*scale+node.Jbias
    
    actv=node.current_to_activity(J.T)
    return x,actv.T


import pylab

x,a=get_tuning_curves(s,apply_sign=True,scale=1)
pylab.figure(figsize=figsize,dpi=300)
pylab.axes((0.2,0.15,0.75,0.8))
for i,v in enumerate(a.T):
    pylab.plot(x,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('stimulus intensity')
pylab.ylim(0,200)
pylab.text(0,170,'attention=1',ha='center')
pylab.figtext(0.01,0.9,'A',zorder=10,weight='bold')
pylab.savefig('fig4a.png',figsize=figsize,dpi=600)


x,a=get_tuning_curves(s,apply_sign=True,scale=0.5)
pylab.figure(figsize=figsize,dpi=300)
pylab.axes((0.2,0.15,0.75,0.8))
for i,v in enumerate(a.T):
    pylab.plot(x,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('stimulus intensity')
pylab.ylim(0,200)
pylab.text(0,170,'attention=0.5',ha='center')
pylab.figtext(0.01,0.9,'B',zorder=10,weight='bold')
pylab.savefig('fig4b.png',figsize=figsize,dpi=600)


x,a=get_tuning_curves(s,apply_sign=True,scale=-1)
pylab.figure(figsize=figsize,dpi=300)
pylab.axes((0.2,0.15,0.75,0.8))
for i,v in enumerate(a.T):
    pylab.plot(x,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('stimulus intensity')
pylab.ylim(0,200)
pylab.text(0,170,'attention=-1',ha='center')
pylab.figtext(0.01,0.9,'C',zorder=10,weight='bold')
pylab.savefig('fig4c.png',figsize=figsize,dpi=600)



pylab.show()

