#*************************************************************************

 #generateData.py - generate sets of nondominated points on fronts
 #                  of different shapes in two and more dimensions
 #
 #version 1.4

 #---------------------------------------------------------------------

 #                      Copyright (c) 2016, 2017
 #               Andreia P. Guerreiro <apg@dei.uc.pt>

 #This program is free software (software libre); you can redistribute
 #it and/or modify it under the terms of the GNU General Public License,
 #version 3, as published by the Free Software Foundation.

 #This program is distributed in the hope that it will be useful, but
 #WITHOUT ANY WARRANTY; without even the implied warranty of
 #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 #General Public License for more details.

 #You should have received a copy of the GNU General Public License
 #along with this program; if not, you can obtain a copy of the GNU
 #General Public License at:
                 #http://www.gnu.org/copyleft/gpl.html
 #or by writing to:
           #Free Software Foundation, Inc., 59 Temple Place,
                 #Suite 330, Boston, MA 02111-1307 USA

#----------------------------------------------------------------------

#    examples: 
#            python generateData.py 100000 2 myDataSets linear
#            python generateData.py 100000 2 myDataSets linear plot
#            python generateData.py 100000 2 myDataSets linear plot-save

#----------------------------------------------------------------------



from __future__ import division
import random
import numpy as np
import sys
import os
import math

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# coordinate values between [0, maxvalue]
maxvalue = 1

# ------------- plot ----------------------


def parallelCoordinates(points):
    fig = plt.figure()
    
    d = len(points[0])
    x = range(1,d+1)
    for pt in points:
        plt.plot(x, pt, 'b-')
    plt.xlabel('dimension')
    plt.xticks(range(1,d+1))
    #plt.show()
    

def plot3D(xs, ys, zs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    #plt.show()
    

def plot2D(xs, ys):
    fig = plt.figure()
    plt.plot(xs, ys, 'o')
    #plt.show()
    

 
def plotSet(points, savePlotTo=None):
    
    d = len(points[0])
    if d == 2:
        plot2D(points[:,0], points[:,1])
    elif d == 3:
        plot3D(points[:,0], points[:,1], points[:,2])
    else:
        parallelCoordinates(points)
        
    if savePlotTo is not None:
        plt.savefig(savePlotTo+'.png')#,
    plt.show()






# ------------- check dominance ----------------------


def getDomAndNDIndices(points):
    domi = []
    n = len(points)
    ndi = range(n)
    for i in xrange(n):
        if i in ndi:
            ndi2 = list(ndi)
            for j in ndi:
                if i != j:
                    if (np.asarray(points[i], dtype=np.float64) <= np.asarray(points[j], dtype=np.float64)).all():
                        domi.append(j)
                        ndi2.remove(j)
        ndi = ndi2
    return (domi, ndi)



# Note: If there are repeated points, all of its copies are considered dominated 
def getDomAndNDIndices2(points):
    doms = (points[:,np.newaxis,:] <= points[np.newaxis,:,:]).all(-1).sum(0) >= 2
    return (np.arange(len(points))[doms], np.arange(len(points))[~doms])


def getRepetitions(points, tol=1e-14):
    ix = np.argsort(points[:,0])
    sortedp = points[ix]
    eqs = (np.abs(sortedp[:-1] - sortedp[1:]) <= tol).any(axis=-1)
    #print eqs, len(eqs), eqs.sum()
    
    return eqs.sum()
    



# -------------- generate data -------------------------



def generateConcave(n, d):
    
    p = abs(np.random.randn(n, d));
    pnorm = np.linalg.norm((p), ord=2, axis=1)
    p = p / pnorm[...,np.newaxis]
    return p



def generateConvex(n, d):
    return 1 - generateConcave(n, d)



def generateLinear(n, d):
    
    p = np.random.uniform(0,1, (n,d))
    p = p/p.sum(-1)[:,np.newaxis]
        
    return p


# Create the wave-? shape in the first two dimensions. If d > 2, the remaining ones are random
def generateWave(n, d, nwaves):

    k=d-1
    maxx = 1
    epsilon = 1e-6
    p = np.random.uniform(0+epsilon,maxx-epsilon, (n,d))
    
    r = 0.2/nwaves
    print "nwaves:", nwaves
    print "r:", r
    angle = -np.pi/4
    ytrans = 1
    x = p[:,0]
    y = r*np.cos(nwaves*2*np.pi*x)-r
    
    x = math.sqrt(2*(maxx**2))*x
    #y = sqrt(2)*y
    x2 = (x*np.cos(angle)-y*np.sin(angle))
    y2 = (x*np.sin(angle)+y*np.cos(angle))+ ytrans
    
    
    p[:,0] = x2
    p[:,1] = y2
        
    return p



def generateCliff(n, d):
    
    if d < 2 or d > 4:
        print "Cliff is available only for d = 3 and d=4!"
        return

    L = np.empty((n,d))
    L[:,:2] = generateConvex(n, 2)  
    
    if d == 3:
        L[:,-1] = np.random.uniform(0,1, (n))
    else: 
        L[:,2:] = generateConvex(n, 2)
            
    return L


    
    
def assureNondominance(L, checkRepOnly=True):
    nrep = getRepetitions(L)
    
    
    # convex, concave, linear, cliff, wave-? data sets do not generate strictly dominated points.
    # There is no need to perform the check below for such sets
    if not checkRepOnly:
        if len(L) <= 10000:
            domi, ndi = getDomAndNDIndices2(L) #fast but more memory consuming
        else:
            domi, ndi = getDomAndNDIndices(L) #slow but needs less memory
        if len(domi) > 0:
            print "There is", len(domi),"dominated points! Only the", len(ndi), "nondominated ones will be printed" 
        L = L[ndi]
        
    return nrep if checkRepOnly else max(nrep, ndi)




def main():
    outPath = sys.argv[1] # output path
    d = int(sys.argv[2]) # d dimensions
    n = int(sys.argv[3]) # n points
    frontType = sys.argv[4] # data type
    plotData = (len(sys.argv) > 5 and sys.argv[5] in ["plot", "plot-save"])
    plotSave = (plotData and sys.argv[5] == "plot-save")
    outFolder = outPath + "/"
    generateData = True
    L = []
    
    while generateData:
        if frontType == 'convex':
            print "generating convex spherical:", n
            L = generateConvex(n, d)
            
        elif frontType == 'concave':
            print "generating concave spherical:", n
            L = generateConcave(n, d)
        
        elif frontType == 'linear':
            print "generating linear:", n
            L = generateLinear(n, d)
        
        elif frontType.startswith("wave-") and d == 2: #wave-nwaves (nwaves is the number of waves, i.e. convex regions) #wave (2d for now)
            print "generating wave:", n
            outFile = frontType #"wave"
            nwaves = int(frontType[5:])
            L = generateWave(n, d, nwaves)
            
        elif frontType == 'cliff' and 3 <= d <= 4:
            if d == 4 and len(L) == 0:
                frontType += "Four"
            print "generating", frontType+":", n
            L = generateCliff(n, d)
            
        else:
            print "wrong front type (%s) and/or number of dimensions (%d)" % (frontType, d)
            return
        
        
        #L should be a nondominated point set but there is a (very) small chance that
        #it contains repeated points. To make sure L does not have repeated points
        # uncomment the line below
        generateData = assureNondominance(L) > 0
        if generateData:
            print "There are either repeated points or at least one point is strictly dominated"
            print "A new data set has to be generated"
    
    
    outFolder += frontType
    outFile = frontType
        
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    
    
    L = maxvalue * L
    
    n = len(L)
    #outFile = outFolder + "/" + outFile + ".1s." + str(d) + "d." + str(n) + ".dat"
    filename = outFolder + "/" + outFile + "." + str(d) + "d." + str(n) + ".dat"
    np.savetxt(filename, L)
    
    
    if plotData: # and d >= 2 and d <= 3:
        savePlotTo = None
        if plotSave:
            plotsFolder = outPath+"/figures"
            if not os.path.exists(plotsFolder):
                os.makedirs(plotsFolder)
            savePlotTo = plotsFolder + "/" + outFile + "." + str(d) + "d." + str(n)
            
        plotSet(L, savePlotTo)
    
    
    
    
if __name__ == '__main__':
    main()
    
    
