#!/usr/bin/env python

# Safety Indicators Calculation

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as pylab
import numpy as np

import random
from time import localtime, strftime

from trafficintelligence import utils, ubc_utils, moving, prediction

def openResultFile(videoFilename, parameters, time, extension):
    filePrefix = utils.cleanFilename(videoFilename)+'/'+utils.cleanFilename(parameters.name)+'-'+time
    out = open(filePrefix+extension,'w')
    out.write('# '+time+' '+str(parameters)+'\n')
    return out

# configuration parameters
frameRate = 15  # frame per second
maxSpeed = 90/3.6/frameRate # speed limit 50 km/h for urban envt, 90km/hr = 25 m/sec for highways
timeHorizon= frameRate*5 # prediction time Horizon = 1.5 s (reaction time) (5 second)
collisionDistanceThreshold= 1.8 # m

# parameters for prediction methods
constantVelocityPredictionParameters = prediction.ConstantPredictionParameters(maxSpeed)

normalAdaptationPredictionParameters = prediction.NormalAdaptationPredictionParameters(maxSpeed, 100, 2./frameRate**2, # m/s2
                                                                                       0.2/frameRate) # rad/s

featurePredictionParameters = prediction.PointSetPredictionParameters(maxSpeed)

# initial version
# -9.1/frameRate**2, # m/s2
# 4.3/frameRate**2, # m/s2
# 0.5/frameRate, # rad/s
def accelerationDistribution(): 
    return random.triangular(-9.1/frameRate**2, 4.3/frameRate**2, 0.)
def steeringDistribution():
    return random.triangular(-0.5/frameRate, 0.5/frameRate, 0.)

evasiveActionPredictionParameters = prediction.EvasiveActionPredictionParameters(maxSpeed, 100, accelerationDistribution, steeringDistribution, False)

featureEvasiveActionPredictionParameters = prediction.EvasiveActionPredictionParameters(maxSpeed, 10, accelerationDistribution, steeringDistribution, True)

dirname = './'
# to run on all video sequences and interacting road users
# filenames = utils.listfiles(dirname, 'avi', remove = True) 
# and change the pairs of interacting road users that will be studied

interactingRoadUsers = {'Miss/0404052336': [(0,3)] # 0,2 and 1 vs 3
                        ,
                        'Incident/0306022035': [(1,3)]
                        ,
                        'Miss/0208030956': [(4,5),(5,7)]
                        }

for videoFilename in interactingRoadUsers.keys():
    print(videoFilename)
    utils.mkdir(utils.cleanFilename(videoFilename))

    # collision points, crossing zones, TTC and PET computations
    objects = ubc_utils.loadTrajectories(dirname+ videoFilename+'-objects.txt')
    features = ubc_utils.loadTrajectories(dirname+ videoFilename+'-features.txt') # needed only if using the feature positions
    time = strftime('%Y-%m-%d-%H-%M-%S')
    for roadUserNumbers in interactingRoadUsers[videoFilename]:
        objects[roadUserNumbers[0]].setFeatures(features)
        objects[roadUserNumbers[1]].setFeatures(features)

    # choose the motion prediction methods to test: the list is [constantVelocityPredictionParameters, normalAdaptationPredictionParameters, featurePredictionParameters]
    for params in [constantVelocityPredictionParameters]:
        print(params.name)
        outCP = openResultFile(videoFilename, params, time, '-collision-points.csv')
        outCZ = openResultFile(videoFilename, params, time, '-crossing-zones.csv')

        for roadUsers in interactingRoadUsers[videoFilename]:
            collisionPoints, crossingZones = params.computeCrossingsCollisions(objects[roadUserNumbers[0]], objects[roadUserNumbers[1]], collisionDistanceThreshold, timeHorizon, True)

        outCP.close()
        outCZ.close()

    # compute probability of unsuccessful evasive action
    # choose the motion prediction methods to test: the list is [evasiveActionPredictionParameters, featureEvasiveActionPredictionParameters]
    for params in []:
        outProba = openResultFile(videoFilename, params, time, '-probability-collision.csv')
        for roadUsers in interactingRoadUsers[videoFilename]:
            collisionProbabilities = params.computeCrossingsCollisions(objects[roadUserNumbers[0]], objects[roadUserNumbers[1]], collisionDistanceThreshold, timeHorizon, True)
        outProba.close()
