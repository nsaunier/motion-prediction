#!/usr/bin/env python

# Plotting results

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as pylab
import numpy as np

import random

from trafficintelligence import utils, ubc_utils, prediction

frameRate = 15.
methodNames = ['constant velocity', 'normal adaptation', 'pointset']

# To run in directory that contains the directories that contain the results (Miss-xx and Incident-xx)
#dirname = '/home/nicolas/Research/Data/kentucky-db/'

interactingRoadUsers = {'Miss/0404052336': [(0,3)] # 0,2 and 1 vs 3
                        #,
                        #'Incident/0306022035': [(1,3)]
                        #,
                        #'Miss/0208030956': [(4,5),(5,7)]
                        }


def getIndicatorName(filename, withUnit = False):
    if withUnit:
        unit = ' (s)'
    else:
        unit = ''
    if 'collision-point' in filename:
        return 'TTC'+unit
    elif 'crossing' in filename:
        return 'pPET'+unit
    elif 'probability' in filename:
        return 'P(UEA)'

def getMethodName(fileprefix):
    if fileprefix == 'constant-velocity':
        return 'Con. Vel.'
    elif fileprefix == 'normal-adaptation':
        return 'Norm. Ad.'
    elif fileprefix == 'point-set':
        return 'Pos. Set'
    elif fileprefix == 'evasive-action':
        return 'Ev. Act.'
    elif fileprefix == 'point-set-evasive-action':
        return 'Pos. Set'

indicator2TimeIdx = {'TTC':2,'pPET':2, 'P(UEA)':3}

def getDataAtInstant(data, i):
    return data[data[:,2] == i]

def getPointsAtInstant(data, i):
    return getDataAtInstant(i)[3:5]

def getIndicator(data, roadUserNumbers, indicatorName):
    if data.ndim ==1:
        data.shape = (1,data.shape[0])

    # find the order for the roadUserNumbers
    uniqueObj1 = np.unique(data[:,0])
    uniqueObj2 = np.unique(data[:,1])
    found = False
    if roadUserNumbers[0] in uniqueObj1 and roadUserNumbers[1] in uniqueObj2:
        objNum1 = roadUserNumbers[0]
        objNum2 = roadUserNumbers[1]
        found = True
    if roadUserNumbers[1] in uniqueObj1 and roadUserNumbers[0] in uniqueObj2:
        objNum1 = roadUserNumbers[1]
        objNum2 = roadUserNumbers[0]
        found = True

    # get subset of data for road user numbers
    if found:
        roadUserData = data[np.logical_and(data[:,0] == objNum1, data[:,1] == objNum2),:]
        if roadUserData.size > 0:
            time = np.unique(roadUserData[:,indicator2TimeIdx[indicatorName]])
            values = {}
            if indicatorName == 'P(UEA)':
                tmp = roadUserData[:,4]
                for k,v in zip(time, tmp):
                    values[k]=v
                return indicators.SeverityIndicator(indicatorName, values, mostSevereIsMax = False, maxValue = 1.), roadUserData
            else:
                for i in time:
                    tmp = getDataAtInstant(roadUserData, i)
                    values[i] = np.sum(tmp[:,5]*tmp[:,6])/np.sum(tmp[:,5])/frameRate
                return indicators.SeverityIndicator(indicatorName, values, mostSevereIsMax = False), roadUserData
    return None, None

saveFig = True

# main section for plotting
for videoFilename in interactingRoadUsers.keys():
    dirname = utils.cleanFilename(videoFilename)
    objects = ubc_utils.loadTrajectories(videoFilename+'-objects.txt')

    # safety indicators
    for roadUserNumbers in interactingRoadUsers[videoFilename]:
        figIndicators = plt.figure()#(figsize = (6,16))
        for plotNum, extension in enumerate([ 'collision-points', 'crossing-zones','probability-collision']):
            filenames = utils.listfiles(dirname, extension+'.csv')
            if plotNum == 0:
                ax1 = figIndicators.add_subplot(3,1, plotNum+1)
            else:
                figIndicators.add_subplot(3,1, plotNum+1, sharex = ax1)
            plt.ylabel(getIndicatorName(extension, True))
            labels = []
            for filename in filenames:
                data = np.loadtxt(dirname+'/'+filename)
                indic, roadUserData = getIndicator(data, roadUserNumbers, getIndicatorName(filename))
                if indic:
                    indic.plot(xfactor = frameRate)
                    labels.append(getMethodName(filename.split('-2012')[0]))
                if plotNum == 2:
                    loc = 2
                else:
                    loc = 0
                plt.legend(labels, loc=loc)
            plt.ylim(ymin = 0.)
            if plotNum == 2:
                plt.xlabel('Time (s)')
        if saveFig:
            plt.savefig(dirname+'-indicators-{0}-{1}.png'.format(roadUserNumbers[0], roadUserNumbers[1]), dpi=150)

    # collision points
    for roadUserNumbers in interactingRoadUsers[videoFilename]:
        figPoints = plt.figure()
        for i, extension in enumerate([ 'collision-points', 'crossing-zones']):
            filenames = utils.listfiles(dirname, extension+'.csv')
            for j,filename in enumerate(filenames):
                if i ==0  and j == 0:
                    ax1 = figPoints.add_subplot(3,2, 2*j+i+1)
                else:
                    figPoints.add_subplot(3,2, 2*j+i+1, sharex = ax1, sharey = ax1)
                data = np.loadtxt(dirname+'/'+filename)
                indic, roadUserData = getIndicator(data, roadUserNumbers, getIndicatorName(filename))
                if indic:
                    #plt.hexbin(roadUserData[:,3], roadUserData[:,4], gridsize = 50)
                    plt.plot(roadUserData[:,3], roadUserData[:,4], 'x')
                    objects[roadUserNumbers[0]].draw('r', withOrigin=True)
                    objects[roadUserNumbers[1]].draw('r', withOrigin=True)
                    plt.axis('equal')
                if j == 0:
                    plt.title(extension.replace('-', ' '))
                if i == 0:
                    plt.ylabel(getMethodName(filename.split('-2012')[0]))

        if saveFig:
            plt.savefig(dirname+'-points-{0}-{1}.png'.format(roadUserNumbers[0], roadUserNumbers[1]), dpi=150)
