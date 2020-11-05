#!/usr/bin/env python3
import click
import xml.etree.ElementTree as ET
import os
import shutil
from dict2xml import dict2xml

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('folders', nargs=-1)
@click.option('-o', '--output', default='.', help='Output folder')  
def concatenateIview_main(folders, output):
    concatenateIview(folders)

def concatenateIview(folders, output='.'):
    #Control the minimal number of folders
    if len(folders) < 2:
        return()

    #copy the first folder
    outputFolder = os.path.join(output, os.path.basename(folders[0]))
    print(outputFolder)
    shutil.copytree(folders[0], outputFolder, dirs_exist_ok=True)
    
    #Read the xml of the first folder
    mainXml = ET.parse(os.path.join(outputFolder, '_Frame.xml'))
    mainXmldict = XmlDictConfig(mainXml.getroot())
    lastSeq = int(mainXmldict['Frames']['Frame'][-1]['Seq'])
    lastDeltaMs = float(mainXmldict['Frames']['Frame'][-1]['DeltaMs'])
    lastCumulativeBeamMU = float(mainXmldict['Frames']['Frame'][-1]['CumulativeBeamMU'])
    #print(xmldict)

    #Copy all other folders
    for folder in folders:
        if folder == folders[0]:
            continue
        currentXml = ET.parse(os.path.join(folder, '_Frame.xml'))
        currentXmldict = XmlDictConfig(currentXml.getroot())
        #list file in that folder
        files = os.listdir(folder)
        jpgFiles = []
        for file in files:
            if file.endswith('.jpg'):
                jpgFiles.append(file)
        jpgFiles.sort()
        
        if not len(jpgFiles) == len(currentXmldict['Frames']['Frame']):
            print("Error, the number of .jpg is not correct")

        for file, xml in zip(jpgFiles, currentXmldict['Frames']['Frame']):
            shutil.copyfile(os.path.join(folder, file), os.path.join(outputFolder, str(lastSeq + int(xml['Seq'])).zfill(5) + file[5:]))
            fileSeq = {
                'Seq': str(lastSeq + int(xml['Seq'])),
                'DeltaMs': str(lastDeltaMs + float(xml['DeltaMs'])), 
                'HasPixelFactor': xml['HasPixelFactor'], 
                'PixelFactor': xml['PixelFactor'], 
                'gantryAngle': xml['gantryAngle'], 
                'CumulativeBeamMU': str(lastCumulativeBeamMU + float(xml['CumulativeBeamMU'])), 
                'IsBeamMuValid': xml['IsBeamMuValid']}
            print(fileSeq)
            mainXmldict['Frames']['Frame'].append(fileSeq)

        #Update last values
        lastSeq = int(mainXmldict['Frames']['Frame'][-1]['Seq'])
        lastDeltaMs = float(mainXmldict['Frames']['Frame'][-1]['DeltaMs'])
        lastCumulativeBeamMU = float(mainXmldict['Frames']['Frame'][-1]['CumulativeBeamMU'])

    outputXml = dict2xml(mainXmldict, wrap="ProjectionSet", indent="\t")
    outputFile = open(os.path.join(outputFolder, "_Frame.xml"), "w")
    outputFile.write(outputXml)
    outputFile.close()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    concatenateIview_main()
