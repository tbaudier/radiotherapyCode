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

def readMonacoXml(file, dataSet, fileNumber):

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

        # Open xml file
        MUbeam = 0.0
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

        return((dataSet, MUbeam))

