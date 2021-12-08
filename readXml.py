#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import matplotlib
matplotlib.get_backend()
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import click
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from matplotlib.widgets import Slider
import itertools
import os

# Set file pathnames
fileDCAT = "/home/tbaudier/marieClaude/positionLameXML/20180426_HerreriasDCATT0.xml"
fileVMAT = "/home/tbaudier/marieClaude/positionLameXML/20180426_HerreriasVMATT0.xml"

# Set variables
gantSpeed = 0
doseRate = 1
beam = 2
seg = 3
x1Diaphragm = 4
x2Diaphragm = 5
y1Diaphragm = 6
y2Diaphragm = 7
leaves = 8
area = 9
meanArea = 10
angles = 11
LSV = 12
AAV = 13
MCS = 14

# Error message
def error(message):
    messagebox.showerror(title="Errors", message=message)
    exit(-1)

#Function to plot the data
def plot(data, category, files):
    #Plot the category from data

    #Plot for simple graphes
    if category <= seg or category == area or category == meanArea or category == LSV or category == AAV:
        colors = itertools.cycle(["r", "b", "g", "c", "m", "y", "k"])
        for fileNumber in range(len(data)):
            X = data[fileNumber][category]['X']
            for i in range(int(len(X)/4)): #Change the first value from 179.9 to -180.0 to have a better plot
                if X[i] >= 179.9:
                    X[i] = -180.0
            Y = data[fileNumber][category]['Y']
            plt.plot(X, Y, color=next(colors), label=os.path.basename(files[fileNumber]))
            #Set labels
            plt.xlabel("Angle [degree]")
            plt.legend()
            if category == gantSpeed:
                plt.title("Gantry Speed")
                plt.ylabel("Speed [?]")
            if category == doseRate:
                plt.title("Dose Rate")
                plt.ylabel("Dose Rate [UM/min]")
            if category == beam:
                plt.title("Beam")
                plt.ylabel("?")
            if category == seg:
                plt.title("Seg")
                plt.ylabel("?")
            if category == area:
                plt.title("Area")
                plt.ylabel("Segment Area [cm2]")
            if category == meanArea:
                plt.title("Mean Area")
                plt.ylabel("Mean Openned Segment Area [cm2]")
            if category == LSV:
                plt.title("Leaf Sequence Variability")
                plt.ylabel("LSV")
            if category == AAV:
                plt.title("Aperture Area Variability")
                plt.ylabel("AAV")

    #Plot X diaphragms on the same graph
    elif category == x1Diaphragm or category == x2Diaphragm:
        if len(data) > 1:
            error("For this plot, select just 1 file")
        X =np.arange(0, len(data[0][5]['X'])*0.250, 0.250) #in seconds
        Y1 = np.asarray(data[0][x1Diaphragm]['Y'])
        Y2 = np.asarray(data[0][x2Diaphragm]['Y'])*-1.0
        plt.plot(X, Y1, 'b', label='Diaphragm 1')
        plt.plot(X, Y2, 'r', label='Diaphragm 2')
        plt.title("X Diaphragm")
        plt.xlabel("Time [s]")
        plt.ylabel("Position of the Diaphragms along X [cm]")
        plt.legend()

    #Plot y diaphragm on the same graph
    elif category == y1Diaphragm or category == y2Diaphragm:
        if len(data) > 1:
            error("For this plot, select just 1 file")
        X =np.arange(0, len(data[0][5]['X'])*0.250, 0.250) #in seconds
        Y1 = np.asarray(data[0][y1Diaphragm]['Y'])
        Y2 = np.asarray(data[0][y2Diaphragm]['Y'])
        plt.plot(X, Y1, 'b', label='Diaphragm 1')
        plt.plot(X, Y2, 'r', label='Diaphragm 2')
        plt.title("Y Diaphragm")
        plt.xlabel("Time [s]")
        plt.ylabel("Position of the Diaphragms along Y [mm]")
        plt.legend()

    #Plot a pair of leaves and update it with a slider
    elif category == leaves:
        if len(data) > 1:
            error("For this plot, select just 1 file")
        X =np.arange(0, len(data[0][5]['X'])*0.250, 0.250) #in seconds
        Y1 = data[0][category][0][0]['Y']
        Y2 = data[0][category][1][0]['Y']
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        Y1plot, = plt.plot(X, Y1, 'b', label='Leaf 1')
        Y2plot, = plt.plot(X, Y2, 'r', label='Leaf 2')
        plt.axis([0, max(X), -2000.0, 2000.0])
        plt.title("Leaf")
        plt.xlabel("Time [s]")
        plt.ylabel("position [mm]")
        plt.legend()

        #Plot the slider:
        axLeaf = plt.axes([0.1, 0.1, 0.8, 0.03])
        sLeaf = Slider(axLeaf, 'Leaf', 1, 80, valinit=0, valstep=1.0)
        #Slider update function
        def updateLeaf(val):
            leafUpdated = int(sLeaf.val)
            Y1plot.set_ydata(data[0][leaves][0][leafUpdated-1]['Y'])
            Y2plot.set_ydata(data[0][leaves][1][leafUpdated-1]['Y'])
            fig.canvas.draw_idle()
        sLeaf.on_changed(updateLeaf)

    #Plot for one angle the X diaphragms and the leaf and update the time with the slider
    elif category == angles:
        if len(data) > 1:
            error("For this plot, select just 1 file")
        time = 0
        angleDegree = data[0][x1Diaphragm]['X'][time]
        X =np.arange(0, len(data[0][5]['X'])*0.250, 0.250) #in seconds
        XdiaphragmXplot = np.arange(-200.0, 201.0, 200.0)
        YdiaphragmX1plot = [data[0][x1Diaphragm]['Y'][time]*10.0] * len(XdiaphragmXplot)
        YdiaphragmX2plot = [data[0][x2Diaphragm]['Y'][time]*-10.0] * len(XdiaphragmXplot)
        XLeafplot = np.arange(200.0, -200.0, -5.0)
        YLeaf1plot = [0.0]*80
        YLeaf2plot = [0.0]*80
        for i in range(len(data[0][leaves][0])):
            YLeaf1plot[i] = data[0][leaves][0][i]['Y'][time]*0.1
            YLeaf2plot[i] = data[0][leaves][1][i]['Y'][time]*0.1
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        diaX1plot, = plt.plot(XdiaphragmXplot, YdiaphragmX1plot, 'r', label='Diaphragm X1')
        diaX2plot, = plt.plot(XdiaphragmXplot, YdiaphragmX2plot, 'm', label='Diaphragm X2')
        leafX1plot, = plt.step(YLeaf1plot, XLeafplot, 'g', where='mid', label='Leaf1')
        leafX2plot, = plt.step(YLeaf2plot, XLeafplot, 'b', where='mid', label='Leaf2')
        plt.title("Angle")
        plt.axis([-200.0, 200.0, -200.0, 200.0])
        plt.xlabel("X position [mm]")
        plt.ylabel("Y position [mm]")
        plt.legend()

        #Slider to update the time
        axTime = plt.axes([0.1, 0.1, 0.8, 0.03])
        sTime = Slider(axTime, 'Time [s]', 0, (len(data[0][5]['X'])-1)*0.250, valinit=0, valstep=0.250)
        plt.title("Angle: " + str(angleDegree) + " degree")
        #Slider update function
        def updateLeaf(val):
            timeUpdated = int(float(sTime.val)/0.250)
            angleDegree = data[0][x1Diaphragm]['X'][timeUpdated]
            diaX1plot.set_ydata([data[0][x1Diaphragm]['Y'][timeUpdated]*10.0] * len(XdiaphragmXplot))
            diaX2plot.set_ydata([data[0][x2Diaphragm]['Y'][timeUpdated]*-10.0] * len(XdiaphragmXplot))
            YLeaf1plot = [0.0]*80
            YLeaf2plot = [0.0]*80
            for i in range(len(data[0][leaves][0])):
                YLeaf1plot[i] = data[0][leaves][0][i]['Y'][timeUpdated]*0.1
                YLeaf2plot[i] = data[0][leaves][1][i]['Y'][timeUpdated]*0.1
            leafX1plot.set_xdata(YLeaf1plot)
            leafX2plot.set_xdata(YLeaf2plot)
            plt.title("Angle: " + str(angleDegree) + " degree")
            fig.canvas.draw_idle()
        sTime.on_changed(updateLeaf)

    plt.show()


#Main function
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--files', default='', help='Pathname to the .xml filenames')
@click.option('--category', default=0, help='Value between 0 and 8')
def readXml(files, category):
    '''
    \b
    Read .xml files for VMAT and DCAT
    And plot the category and leaf (if it is leaf)
    For category:
     - 0: Grantry Speed
     - 1: Dose Rate
     - 2: Beam
     - 3: Seg
     - 4: X1 Diaphragm
     - 5: X2 Diaphragm
     - 6: Y1 Diaphragm
     - 7: Y2 Diaphragm
     - 8: Leaf
     - 9: Open area
     - 10: Mean openned area
     - 11: angle
     - 12: LSV (leaf sequence variability)
     - 13: AAV (aperture area variability)
     - 14: MCS (modulation complexity score)
    '''

    #Select the xml file if file is empty
    if files == '':
        Tk().withdraw()
        files = filedialog.askopenfilenames(title = "Select xml file(s)",filetypes = (("xml files","*.xml"),("all files","*.*")))
        if files == '':
            error("Choose a xml file")
    else:
        files = [files]

    #Initialize variable
    nbSideLeaf = 2
    nbLeaf = 80
    leafWidth = 50 #1/10 mm
    leafGap = 5 #1/10mm if 2 leaves are separated < leafGap then they are closed

    # Set the structure
    dataSet = [None]*len(files)
    for i in range(len(files)):
        dataSet[i] = [None]*15
        dataSet[i][gantSpeed] = {'X': [], 'Y': []}
        dataSet[i][doseRate] = {'X': [], 'Y': []}
        dataSet[i][beam] = {'X': [], 'Y': []}
        dataSet[i][seg] = {'X': [], 'Y': []}
        dataSet[i][x1Diaphragm] = {'X': [], 'Y': []}
        dataSet[i][x2Diaphragm] = {'X': [], 'Y': []}
        dataSet[i][y1Diaphragm] = {'X': [], 'Y': []}
        dataSet[i][y2Diaphragm] = {'X': [], 'Y': []}
        dataSet[i][leaves] = [[{'X': [], 'Y': []} for i in range(nbLeaf)] for j in range(nbSideLeaf)]
        dataSet[i][area] = {'X': [], 'Y': []}
        dataSet[i][meanArea] = {'X': [], 'Y': []}
        dataSet[i][LSV] = {'X': [], 'Y': []}
        dataSet[i][AAV] = {'X': [], 'Y': []}
        dataSet[i][MCS] = 0.0

    fileNumber = 0
    for file in files:
        MUbeam = 0.0
        # Open xml file
        tree = ET.parse(file)
        root = tree.getroot()

        # Read the file
        for child in root:
            if child.tag == 'series':
                # Look for the category name
                split = re.split(',|/', child.attrib['title'])
                categoryNumber = 0
                if 'Gant speed' in split[2]:
                    categoryNumber = gantSpeed
                elif 'D' in split[2] and 'rate' in split[3]:
                    categoryNumber = doseRate
                elif 'Beam' in split[2]:
                    categoryNumber = beam
                elif 'Seg' in split[2]:
                    categoryNumber = seg
                elif 'X1 Diaphragm' in split[2]:
                    categoryNumber = x1Diaphragm
                elif 'X2 Diaphragm' in split[2]:
                    categoryNumber = x2Diaphragm
                elif 'Y1 Diaphragm' in split[2]:
                    categoryNumber = y1Diaphragm
                elif 'Y2 Diaphragm' in split[2]:
                    categoryNumber = y2Diaphragm
                # If leaf, look for the number of the leaf
                # sideLeaf is 1 or 2, and leafPosition is between 1 and 80
                elif 'Leaf' in split[2]:
                    categoryNumber = leaves
                    yPosition = split[2].find('Y')
                    sideLeaf = int(split[2][yPosition+1])
                    leafPosition = int(split[2][yPosition+2:])
                else:
                    print('I do not know this category' + split)
                    exit(-1)

                for child2 in child:
                    for child3 in child2:
                        if child3.tag == 'point':
                            # Sort X and Y data into the data structure according the current category
                            if categoryNumber != leaves:
                                dataSet[fileNumber][categoryNumber]['X'].append(float(child3.attrib['X']))
                                dataSet[fileNumber][categoryNumber]['Y'].append(float(child3.attrib['Y']))
                                if categoryNumber == doseRate:
                                    MUbeam += float(child3.attrib['Y'])
                            else:
                                dataSet[fileNumber][categoryNumber][sideLeaf-1][leafPosition-1]['X'].append(float(child3.attrib['X']))
                                dataSet[fileNumber][categoryNumber][sideLeaf-1][leafPosition-1]['Y'].append(float(child3.attrib['Y']))

        #Look for the number of element, ie. max of elements
        nbXElement = 0
        for i in range(0,7):
            if nbXElement < len(dataSet[fileNumber][i]['X']):
                nbXElement = len(dataSet[fileNumber][i]['X'])
        for i in range(0, nbSideLeaf):
            for j in range(0, nbLeaf):
                if nbXElement < len(dataSet[fileNumber][leaves][i][j]['X']):
                    nbXElement = len(dataSet[fileNumber][i]['X'])

        #Look if the have the same number of element
        #else repeat the first element
        for i in range(0,7):
            if nbXElement != len(dataSet[fileNumber][i]['X']):
                for j in range(len(dataSet[fileNumber][i]['X']), nbXElement):
                    dataSet[fileNumber][i]['X'].insert(0, dataSet[fileNumber][i]['X'][0])
                    dataSet[fileNumber][i]['Y'].insert(0, dataSet[fileNumber][i]['Y'][0])
        for i in range(0, nbSideLeaf):
            for j in range(0, nbLeaf):
                if nbXElement != len(dataSet[fileNumber][leaves][i][j]['X']):
                    for k in range(len(dataSet[fileNumber][leaves][i][j]['X']), nbXElement):
                        dataSet[fileNumber][leaves][i][j]['X'].insert(0, dataSet[fileNumber][leaves][i][j]['X'][0])
                        dataSet[fileNumber][leaves][i][j]['Y'].insert(0, dataSet[fileNumber][leaves][i][j]['Y'][0])

        #Compute area and mean area
        for i in range(0, nbXElement):
            dataSet[fileNumber][area]['X'].append(dataSet[fileNumber][leaves][0][0]['X'][i])
            dataSet[fileNumber][meanArea]['X'].append(dataSet[fileNumber][leaves][0][0]['X'][i])
            #Compute the limits due to the diaphragms in 1/10mm
            x1limit = dataSet[fileNumber][x1Diaphragm]['Y'][i]*100.0
            x2limit = dataSet[fileNumber][x2Diaphragm]['Y'][i]*-100.0
            y1limit = dataSet[fileNumber][y1Diaphragm]['Y'][i]
            y2limit = dataSet[fileNumber][y2Diaphragm]['Y'][i]*-1.0
            dataSet[fileNumber][area]['Y'].append(0.0)
            #Sum on the 80 leaves
            nbOpennedLeaf = 0
            for k in range(0, nbLeaf):
                #Look if the leaf is in the open part of the diaphragm
                posY1 = dataSet[fileNumber][leaves][0][k]['Y'][i]
                posY2 = dataSet[fileNumber][leaves][1][k]['Y'][i]
                posX1 = k*leafWidth-2000.0
                posX2 = (k+1)*leafWidth-2000.0
                if posY1 > y1limit:
                    posY1 = y1limit
                if posY1 < y2limit:
                    posY1 = y2limit
                if posY2 < y2limit:
                    posY2 = y2limit
                if posY2 > y1limit:
                    posY2 = y1limit
                if posX1 > x1limit:
                    posX1 = x1limit
                if posX1 < x2limit:
                    posX1 = x2limit
                if posX2 > x1limit:
                    posX2 = x1limit
                if posX2 < x2limit:
                    posX2 = x2limit
                if (posY1 - posY2) <= leafGap:
                    posY1 = posY2
                if (abs((posY1 - posY2)*(posX2 - posX1)) > 0):
                    nbOpennedLeaf += 1
                dataSet[fileNumber][area]['Y'][i] += abs((posY1 - posY2)*(posX2 - posX1))
            dataSet[fileNumber][area]['Y'][i] *= 1.0/10000.0 #in cm2
            dataSet[fileNumber][meanArea]['Y'].append(dataSet[fileNumber][area]['Y'][i] / nbOpennedLeaf) #mean openned area

        #Compute LSV & AAV
        tmpPosMaxAAV = [-2000.0]*nbLeaf
        tmpPosMinAAV = [2000.0]*nbLeaf
        for i in range(0, nbXElement):
            dataSet[fileNumber][LSV]['X'].append(dataSet[fileNumber][leaves][0][0]['X'][i])
            dataSet[fileNumber][AAV]['X'].append(dataSet[fileNumber][leaves][0][0]['X'][i])
            #Compute the limits due to the diaphragms in 1/10mm
            x1limit = dataSet[fileNumber][x1Diaphragm]['Y'][i]*100.0
            x2limit = dataSet[fileNumber][x2Diaphragm]['Y'][i]*-100.0
            y1limit = dataSet[fileNumber][y1Diaphragm]['Y'][i]
            y2limit = dataSet[fileNumber][y2Diaphragm]['Y'][i]*-1.0
            tmpPosMaxLSV = -2000
            tmpPosMinLSV = 2000
            N = 0
            posSumLeft = 0
            posSumRight = 0
            posSum = 0
            for k in range(0, nbLeaf-1):
                #Look if the leaf is in the open part of the diaphragm
                #Look for nbLeaf -1 leaves because we need the position of leaf n+1
                posY1 = dataSet[fileNumber][leaves][0][k]['Y'][i]
                posY2 = dataSet[fileNumber][leaves][1][k]['Y'][i]
                posX1 = k*leafWidth-2000.0
                posX2 = (k+1)*leafWidth-2000.0
                if posY1 < y2limit:
                    continue
                if posY2 > y1limit:
                    continue
                if posX1 > x1limit:
                    continue
                if posX2 < x2limit:
                    continue

                #The leaf is in the open part and is openned
                N += 1
                posSumRight += posY1 - dataSet[fileNumber][leaves][0][k+1]['Y'][i]
                posSumLeft += posY2 - dataSet[fileNumber][leaves][1][k+1]['Y'][i]
                posSum += posY1 - posY2

                #Check min/max
                if posY2 < tmpPosMinLSV:
                    tmpPosMinLSV = posY2
                if posY1 > tmpPosMaxLSV:
                    tmpPosMaxLSV = posY1
                if posY2 < tmpPosMinAAV[k]:
                    tmpPosMinAAV[k] = posY2
                if posY1 > tmpPosMaxAAV[k]:
                    tmpPosMaxAAV[k] = posY1

            dataSet[fileNumber][LSV]['Y'].append((1-posSumLeft/(N*(tmpPosMaxLSV-tmpPosMinLSV)))*((1-posSumRight/(N*(tmpPosMaxLSV-tmpPosMinLSV)))))
            dataSet[fileNumber][AAV]['Y'].append(posSum)

        #Still compute AAV
        posSumMax = 0.0
        for k in range(0, nbLeaf):
            if tmpPosMaxAAV[k] != -2000.0 or tmpPosMinAAV[k] != 2000.0:
                posSumMax += tmpPosMaxAAV[k] - tmpPosMinAAV[k]

        for i in range(0, nbXElement):
            dataSet[fileNumber][AAV]['Y'][i] /= posSumMax

        #Compute MCS
        dataSet[fileNumber][MCS] = 0.0
        for i in range(0, nbXElement):
            dataSet[fileNumber][MCS] += dataSet[fileNumber][AAV]['Y'][i]*dataSet[fileNumber][LSV]['Y'][i]*dataSet[fileNumber][doseRate]['Y'][i]/MUbeam

        fileNumber += 1

    #Plot the data if not MCS
    if category == MCS:
        MCStotal = 0.0
        for i in range(len(files)):
            print("beam (" + os.path.basename(files[i]) + "): " + str(dataSet[i][MCS]))
            MCStotal += dataSet[i][MCS]
        MCStotal /= len(files)
        print("mean: " + str(MCStotal))
    else:
        plot(dataSet, category, files)

if __name__ == "__main__":
        readXml()
