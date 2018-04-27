from nef import *
import numpy
import pylab

figsize=(4,2.5)

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


def get_tuning_curves(node,distance=1):
    dtheta=0.05
    theta=numpy.arange(-numpy.pi,numpy.pi,dtheta)
    x=numpy.array([numpy.sin(theta),numpy.cos(theta)])
    x2=numpy.dot(node.basis,x)
    J=node.alpha*x2.T*distance+node.Jbias
    actv=node.current_to_activity(J.T)
    return theta,actv.T

def get_all_tuning_curves(node,neuron):
    dx=0.1
    xx=numpy.arange(-1,1,dx)
    yy=numpy.arange(-1,1,dx)
    x,y=numpy.meshgrid(xx,yy)

    z=[]
    for i in range(len(x)):
        xxx=numpy.array([x[i],y[i]])
        x2=numpy.dot(node.basis[neuron],xxx)
        J=node.alpha[neuron]*x2.T+node.Jbias[neuron]
        actv=node.current_to_activity(J.T)
        z.append(actv)

    
    return x,y,numpy.array(z)




s=VectorNode(2)
s.configure(12,saturation_range=(100,200),t_ref=0.002,t_rc=0.02,threshold_coverage=0.4)



x,a=get_tuning_curves(s)
pylab.figure(figsize=figsize,dpi=300)
pylab.axes((0.15,0.2,0.8,0.7))
for i,v in enumerate(a.T):
    pylab.plot(x*180/numpy.pi,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('represented angle (degrees)')
pylab.xlim(-180,180)
pylab.xticks([-180,-90,0,90,180])
pylab.figtext(0.01,0.9,'A',zorder=10,weight='bold')
pylab.savefig('fig2a.png',figsize=figsize,dpi=600)



x,a=get_tuning_curves(s,distance=0.6)
pylab.figure(figsize=figsize,dpi=300)
pylab.axes((0.15,0.2,0.8,0.7))
for i,v in enumerate(a.T):
    pylab.plot(x*180/numpy.pi,v,linestyle=linestyle(i),color=color(i),linewidth=linewidth(i))
pylab.ylabel('firing rate (Hz)')    
pylab.xlabel('represented angle (degrees)')
pylab.ylim(0,200)
pylab.xlim(-180,180)
pylab.xticks([-180,-90,0,90,180])
pylab.figtext(0.01,0.9,'B',zorder=10,weight='bold')
pylab.text(0,170,'decreased speed',ha='center')
pylab.savefig('fig2b.png',figsize=figsize,dpi=600)


s=VectorNode(2)
s.configure(1,basis=[[0.8,0.6]],saturation_range=(100,200),t_ref=0.002,t_rc=0.02,threshold_coverage=0.4,thresholds=[-0.1])


import mpl_toolkits.mplot3d.axes3d as p3

from numpy import *
x,y,z=get_all_tuning_curves(s,0)

fig=pylab.figure(figsize=figsize,dpi=200)
ax = p3.Axes3D(fig,rect=[0,0.1,0.9,0.9],azim=-61,elev=21)
ax.plot_wireframe(x,y,z,color='k')
ax.set_xlabel('\n\nX',size=12)
ax.set_ylabel('\n\nY',size=12)
ax.set_zlabel('\n\n\nfiring rate (Hz)',size=12)
pylab.figtext(0.01,0.9,'C',zorder=10,weight='bold')
pylab.savefig('fig2c.png',figsize=figsize,dpi=600)
pylab.show()

