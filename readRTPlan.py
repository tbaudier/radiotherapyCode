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
import pydicom

def readDicomRTPlan(file, dataSet, fileNumber):

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

        nbSideLeaf = 2
        nbLeaf = 80
        leafWidth = 50 #1/10 mm
        leafGap = 5 #1/10mm if 2 leaves are separated < leafGap then they are closed

        # Open xml file
        MUbeam = 0.0
        ds = pydicom.dcmread(file)[0x300a, 0x00b0].value[0][0x300a, 0x0111]

        # Read the file
        # for each control point
        for cp in ds.value:
            #print(cp)
            dataSet[fileNumber][gantSpeed]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][gantSpeed]['Y'].append(0)
            dataSet[fileNumber][doseRate]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][doseRate]['Y'].append(0.0)
            MUbeam += float(0.0)
            dataSet[fileNumber][beam]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][beam]['Y'].append(0)
            dataSet[fileNumber][seg]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][seg]['Y'].append(0)
            dataSet[fileNumber][x1Diaphragm]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][x1Diaphragm]['Y'].append(cp[0x300a, 0x011a].value[0][0x300a, 0x011c].value[0])
            dataSet[fileNumber][x2Diaphragm]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][x2Diaphragm]['Y'].append(cp[0x300a, 0x011a].value[0][0x300a, 0x011c].value[1])
            dataSet[fileNumber][y1Diaphragm]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][y1Diaphragm]['Y'].append(2000)
            dataSet[fileNumber][y2Diaphragm]['X'].append(cp[0x300a, 0x011e].value)
            dataSet[fileNumber][y2Diaphragm]['Y'].append(2000)
            for i in range(80):
                dataSet[fileNumber][leaves][0][i]['X'].append(i)
                dataSet[fileNumber][leaves][0][i]['Y'].append(cp[0x300a, 0x011a].value[1][0x300a, 0x011c].value[i]*10)
            for i in range(80):
                dataSet[fileNumber][leaves][1][i]['X'].append(i)
                dataSet[fileNumber][leaves][1][i]['Y'].append(cp[0x300a, 0x011a].value[1][0x300a, 0x011c].value[80+i]*10)
            
        return((dataSet, MUbeam))

