import gatetools as gt
import itk
import numpy as np
import copy
import pydicom
from datetime import datetime
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag

def insertTag(dataset, tag, value, type):
    if tag in dataset:
        dataset[tag].value = value
    else:
        dataset[tag] = pydicom.DataElement(tag, type, value)


def convertTagValue(value, VRtype):
    if VRtype in ["AE", "AS" , "AT", "CS", "DA", "DS", "DT", "IS", "LO", "LT", "OB", "OD", "OF", "OW", "PN", "SH", "ST", "TM", "UI", "UN", "UT"]:
        return str(value)
    elif VRtype in ["SL", "SS", "UL", "US"]:
        return int(value)
    elif VRtype in ["FL", "FD"]:
        return float(value)

CTDicomPath = "C:/Users/DIFRANCF/Downloads/output/output/Monaco_CBCT/2.CT.DCM"
mhdCBCTPath = "C:/Users/DIFRANCF/Downloads/output/output/CBCT.mha"
outputDicomPath = "C:/Users/DIFRANCF/Downloads/output/output/"
inputImage = itk.imread(mhdCBCTPath)

#gt.writeDicom(inputImage, CTDicomPath, outputDicomPath, True)

# Scale the input:
inputArray = itk.array_from_image(inputImage)
#inputArray[inputArray > 4000] = 4000
max = np.amax(inputArray)
min = np.amin(inputArray)
scaling = (max - min)/(2**16-1)
intercept = min
inputArray = (inputArray - intercept)/scaling
inputArray = (inputArray).astype(np.uint16)
#intercept = intercept - 1024
#min = min - 1024
#max = max - 1024
inputImageChar = itk.image_from_array(inputArray)

#Write the input as a new dicom
imageIO = itk.GDCMImageIO.New()
writer = itk.ImageSeriesWriter[type(inputImageChar), itk.Image[itk.US,2]].New()
writer.SetInput(inputImageChar)
writer.SetImageIO(imageIO)
nameGenerator = itk.NumericSeriesFileNames.New()
format = outputDicomPath + "%03d." + "dcm"
nameGenerator.SetSeriesFormat(format)
nameGenerator.SetStartIndex(0)
nameGenerator.SetEndIndex(inputImage.GetLargestPossibleRegion().GetSize()[2]-1)
nameGenerator.SetIncrementIndex(1)
#print(nameGenerator.GetFileNames())
writer.SetFileNames(nameGenerator.GetFileNames())
writer.Update()


#Open the new dicom and change some dicom tags according dicom input or not
index = 0
now = datetime.now()
for slice in nameGenerator.GetFileNames():
    dsImage = pydicom.dcmread(slice, force=True)
    dsDicom = pydicom.dcmread(CTDicomPath, force=True)
    dsOutput = copy.deepcopy(dsImage)


    insertTag(dsOutput, 0x00080023, now.strftime("%Y%m%d"), 'DA') #Content Date
    insertTag(dsOutput, 0x00080033, now.strftime("%H%M%S") + ".000000", 'TM') #Content Time
    insertTag(dsOutput, 0x00080060, "CT", 'CS') #Content Time
    insertTag(dsOutput, 0x00100020, "CT 1814", 'LO')
    insertTag(dsOutput, 0x00100020, "1808899", 'LO')
    insertTag(dsOutput, 0x00100030, "19381108", 'DA')
    insertTag(dsOutput, 0x00100040, "M", 'CS')
    #insertTag(dsOutput, 0x00101010, "79Y", 'AS')
    #insertTag(dsOutput, 0x00200013, index, 'IS')
    #insertTag(dsOutput, 0x00201041, inputImageChar.GetSpacing()[2]*index, 'DS')
    #insertTag(dsOutput, 0x00080008, "['DERIVED']", 'CS')
    #insertTag(dsOutput, 0x00080012, "20180925", 'DA')
    #insertTag(dsOutput, 0x00080013, "110853", 'TM')
    #insertTag(dsOutput, 0x00080014, "1.3.46.423632.336117", 'UI')
    #insertTag(dsOutput, 0x00080016, "1.2.840.10008.5.1.4.1.1.2", 'UI')
    #newSOPInstanceUID = pydicom.uid.generate_uid()
    #insertTag(dsOutput, 0x00080018, newSOPInstanceUID, 'UI')
    #insertTag(dsOutput, 0x00080021, "20200728", 'DA')
    #insertTag(dsOutput, 0x00080022, "20181113", 'DA') #Date
    #insertTag(dsOutput, 0x00080031, "100501", 'TM')
    #insertTag(dsOutput, 0x00080032, "151120", 'TM') #Time
    #insertTag(dsOutput, 0x00080070, "ELEKTA", 'LO')
    #insertTag(dsOutput, 0x00080080, "XVI", 'LO')
    del dsOutput[0x00080064]
    del dsOutput[0x00281054]

    #insertTag(dsOutput, 0x00081010, "VersaHD_XVI", 'SH')
    #insertTag(dsOutput, 0x00081030, "VersaHD Treatmen:Tx Plan for 1505126 on 07-24-2020", 'LO') #Change with real patient's data
    #insertTag(dsOutput, 0x0008103e, "CBCT(#phase:10) Option 3; One phase(1)", 'LO')
    #insertTag(dsOutput, 0x00081090, "Elekta XVI", 'LO')
    #insertTag(dsOutput, 0x00081150, "RT Image Storage", 'UI')
    #insertTag(dsOutput, 0x00081155, "1.3.46.423632.3361172020728134028719.41", 'UI')

    #insertTag(dsOutput, 0x00180060, "120.0", 'DS')
    #insertTag(dsOutput, 0x00180088, inputImageChar.GetSpacing()[2], 'DS')
    #insertTag(dsOutput, 0x00185100, "HFS", 'CS')
    #insertTag(dsOutput, 0x00200032, [inputImageChar.GetOrigin()[0], inputImageChar.GetOrigin()[1], inputImageChar.GetOrigin()[0] + inputImageChar.GetSpacing()[2]*index], 'DS')
    #insertTag(dsOutput, 0x00200037, [1, 0, 0, 0, 1, 0], 'DS')

    #insertTag(dsOutput, 0x00280106, 0, 'US')
    #insertTag(dsOutput, 0x00280107, 65535, 'US')
    #insertTag(dsOutput, 0x00281052, intercept, 'DS') #Rescale Intercept
    #insertTag(dsOutput, 0x00281053, scaling, 'DS') #Rescale Slope
    #ds.add_new(0x00100050, 'CIAOCIAO', '12345')

    index += 1

    dsOutput.save_as(slice)

