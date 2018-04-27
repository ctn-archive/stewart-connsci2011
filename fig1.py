from nef import *

linestyles=['-','--']
colors=['0.0','0.3','0.6']
linewidths=[1,2]

def color(index):
    return colors[index%len(colors)]
def linestyle(index):
    index=index/2
    return linestyles[index%len(linestyles)]
def linewidth(index):
    return linewidths[index%len(linewidths)]

s=ScalarNode()
s.configure(12,saturation_range=(100,200),t_ref=0.002,t_rc=0.02,threshold_coverage=0.7)
import numpy
def get_tuning_curves(node,dx=0.005,apply_sign=False):
    x=numpy.arange(node.min,node.max,dx)
    alpha=node.alpha
    if apply_sign:
        sign=numpy.sign(node.basis[:,0])
        sign.shape=sign.shape[0]
        alpha=alpha*sign
            
    J=numpy.outer(alpha,x).T+node.Jbias
    
    actv=node.current_to_activity(J.T)
    return x,actv.T


x,a=get_tuning_curves(s,apply_sign=True)




import pylab
pylab.figure(figsize=(5,2.5),dpi=300)
pylab.axes((0.15,0.2,0.8,0.7))
for i,v in enumerate(a.T):
    pylab.plot(x,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('represented value (x)')
pylab.savefig('fig1.png',figsize=(5,2.5),dpi=600)
pylab.show()

