#!/usr/bin/env python

# Plotting predicted trajectories according to various methods

import matplotlib.pyplot as plt
import matplotlib.mlab as pylab
import numpy as np

from trafficintelligence import utils, ubc_utils, prediction

frameRate = 15  # frame per second
maxSpeed = 90/3.6/frameRate # speed limit 50 km/h for urban envt, 90km/hr = 25 m/sec for highways
timeHorizon= frameRate*5 # prediction time Horizon = 1.5 s (reaction time) (5 second)

dirname = '/home/nicolas/Research/Data/kentucky-db/'
interactingRoadUsers = {'Miss/0404052336': [(0,3)], # 0,2 and 1 vs 3 # severe
                        'Incident/0306022035': [(1,3)],
                        'Miss/0208030956': [(4,5),(5,7)]} # 4-5 - severe

# use accident for example of the predicted trajectories
constantVelocityPredictionParameters = prediction.ConstantPredictionParameters(maxSpeed)

normalAdaptationPredictionParameters = prediction.NormalAdaptationPredictionParameters(maxSpeed, 10, 2./frameRate**2, # m/s2
                                                                                       0.2/frameRate) # rad/s

featurePredictionParameters = prediction.PointSetPredictionParameters(maxSpeed)

evasiveActionPredictionParameters = prediction.EvasiveActionPredictionParameters(maxSpeed, 10, -9.1/frameRate**2, # m/s2
                                                                                 4.3/frameRate**2, # m/s2
                                                                                 0.5/frameRate, # rad/s
                                                                                 False)

featureEvasiveActionPredictionParameters = prediction.EvasiveActionPredictionParameters(maxSpeed, 10, -9.1/frameRate**2, # m/s2
                                                                                        4.3/frameRate**2, # m/s2
                                                                                        0.5/frameRate, # rad/s
                                                                                        True)

# chosen instant for the video and interacting road users
instant = 50
videoFilename = 'Incident/0306022035'

objects = ubc_utils.loadTrajectories(dirname+ videoFilename+'-objects.txt')
features = ubc_utils.loadTrajectories(dirname+ videoFilename+'-features.txt') # needed only if using the feature positions
for roadUserNumbers in interactingRoadUsers[videoFilename]:
    objects[roadUserNumbers[0]].setFeatures(features)
    objects[roadUserNumbers[1]].setFeatures(features)

fig = plt.figure(figsize = (7,9))
subplotLocations = [1, 3, 5, 2, 4]
methodNames = ['Constant Velocity', 'Normal Adaptation', 'Position Set', 'Evasive Action', 'Evasive Action Position Set']
for i, params in enumerate([constantVelocityPredictionParameters, normalAdaptationPredictionParameters, featurePredictionParameters, evasiveActionPredictionParameters, featureEvasiveActionPredictionParameters]):
    if i == 0:
        ax1 = fig.add_subplot(3,2, subplotLocations[i])
    else:
        fig.add_subplot(3,2, subplotLocations[i], sharex = ax1, sharey = ax1)
    predictedTrajectories1 = params.generatePredictedTrajectories(objects[roadUserNumbers[0]], instant)
    predictedTrajectories2 = params.generatePredictedTrajectories(objects[roadUserNumbers[1]], instant)

    for et1 in predictedTrajectories1:
        et1.predictPosition(timeHorizon)
        et1.draw('rx', timeStep = 5)
    for et2 in predictedTrajectories2:
        et2.predictPosition(timeHorizon)
        et2.draw('bx', timeStep = 5)

    objects[roadUserNumbers[0]].draw('k', withOrigin = True, linewidth=1.5)
    objects[roadUserNumbers[1]].draw('k', withOrigin = True, linewidth=1.5)
    plt.ylabel(methodNames[i])
fig.subplots_adjust(wspace = 0.3)   
plt.axis('equal')
plt.savefig(utils.cleanFilename(videoFilename)+'-predicted-trajectories{0}.png'.format(instant), dpi = 150)

def playVideos(renameFigure = False):
    import cvutils
    for videoFilename in interactingRoadUsers.keys():
        print(videoFilename)
        objects = ubc_utils.loadTrajectories(dirname+ videoFilename+'-objects.txt')
        for roadUserNumbers in interactingRoadUsers[videoFilename]:
            print(roadUserNumbers)
            cvutils.displayTrajectories(dirname+ videoFilename+'.avi', [objects[i] for i in roadUserNumbers], np.linalg.inv(np.loadtxt(dirname+ videoFilename+'-homography.txt')))
            if renameFigure:
                import os
                os.rename('image.png', utils.cleanFilename(videoFilename)+'{0}-{1}-objects.png'.format(roadUserNumbers[0], roadUserNumbers[1]))
