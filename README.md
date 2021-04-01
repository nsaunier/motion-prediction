  Mohamed and Saunier - TRB 2013 

Motion Prediction Methods for Surrogate Safety Analysis
=======================================================

TRB 92nd Annual Meeting (2013), paper reference 13-4647
-------------------------------------------------------

### Mohamed Gomaa Mohamed and Nicolas Saunier

**Abstract:** Despite the rise in interest for surrogate safety analysis, little work has been done to understand and test the impact of the methods for motion prediction which are needed to identify whether two road users are on a collision course and to compute many surrogate safety indicators such as the time to collision (TTC). The default, unjustified method used in much of the literature is prediction at constant velocity. In this paper, a generic framework is presented to predict road users' future positions depending on their current position and their choice of acceleration and direction. This results in the possibility of generating many predicted trajectories by sampling distributions of acceleration and direction. Three safety indicators, the TTC, an extended version of predicted post encroachment time pPET and a new indicator measuring the probability that the road users attempting evasive actions fail to avoid the collision P(UAE), are computed over all predicted trajectories. These methods and indicators are illustrated on four case studies of lateral road user interactions. The evidence suggests that the prediction method based on the use of a set of initial positions seems to be the most robust. The last contribution of this paper is to make all the data and code used for this paper available (the code as open source) to enable reproducibility and to start a collaborative effort to compare and improve the methods for surrogate safety analysis.

This page presents all the necessary information to replicate the results presented in this paper, the code, available under the open source [MIT license](LICENSE.md) and the data used as a support for discussion in the paper.

Data
----

Four traffic events were used in this paper to illustrate the impact of the method used for motion prediction to identify potential collision points and compute indicators such as the TTC, the pPET and P(UEA). The trajectories extracted from the videos are provided, in two files for each video sequence (there are three video sequence, with case study 3 and 4 in the same sequence Miss/0208030956). The trajectory data is stored in two files for each sequence, one for features (\-features.txt) and one for the vehicles or "objects" (\-objects.txt). In these text files, each trajectory data is written one after the other (features and vehicles) (it is replaced in the new projects by a sqlite database, see [Traffic Intelligence project](https://trafficintelligence.confins.net)):

sequence\_num first\_instant last\_instant
X1 X2 ...
Y1 Y2 ...
Vx1 Vx2 ...
Vy1 Vy2 ...
%
...

where Xi and Yi and Vxi and Vyi are respectively the position coordinates and the velocity vector components at index i (counting 0 as the index of the first measurement, the corresponding frame number is first\_instant+i). The homography files, ie the 3x3 matrix that is used to project from image space (in pixels) to the ground plane (in meters), is also provided in the corresponding \-homography.txt files. All files, 3 per video sequence, are in the `Miss` and `Incident` subdirectories respectively for conflicts and collisions.

Code
----

The code has been written in the open source and cross-platform Python language and depends on larger open source project called [Traffic Intelligence](https://trafficintelligence.confins.net). There are two ways to get the necessary files, the first being to downlowad a snapshot of the last version (click on the "get source" link on the project webpage), the second being to clone the code repository using the [Mercurial version control software](http://mercurial.selenic.com/) (`$ hg clone http://132.207.98.161:3000/ <destination directory>`). The python subdirectory must be in your path to be able to import the modules. The [NumPy](http://numpy.scipy.org/) and [Matplotlib](http://matplotlib.sourceforge.net/) libraries must also be installed.

The script that generates the results is called [process-extrapolation-hypotheses.py](process-extrapolation-hypotheses.py). Two other scripts are provided to plot the graphics, [plot-results.py](plot-results.py) and [other-figures.py](other-figures.py). The only thing that you should have to change should be the dirname variable that should contain the directories Miss and Incident extracted from the data archive. The results are stored in csv files for the collision points, crossing zones respectively with pPET and TTC values (\-collision-points.csv and \-crossing-zones.csv files) and probabilities of unsucessful evasive action (\-probability-collision.csv files) in subfolder for each video sequence. There is a file for each motion prediction method, and each line correspond to measurements at a given instant. The formats are the following:

*   points files:
    
    vehicle\_id1, vehicle\_id2, instant, x\_coordinate, y\_coordinate, probability, indicator\_value
    
*   collision probability files:
    
    vehicle\_id1, vehicle\_id2, nSamples, instant, collision\_probability
    

Extrapolation parameters are saved as a comment on the first line (line starting with #) so that the parameters used to generate the results can be traced back once the files are generated. The date and time are appended to the filenames of all result files so that the script can be started multiple times in parallel (eg as many times as the computer has cores).

Please do not hesitate to contact us if you have any question.
