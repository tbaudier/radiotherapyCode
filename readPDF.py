import pdfminer.high_level
import openpyxl
from openpyxl import Workbook
#Read the pdf
text = pdfminer.high_level.extract_text('/Users/tbaudier/guillaume/2005485_SegmentDetail.pdf')

##Read the pdf
#Separate all pages
pages = text.split('\x0c')
#print(pages)

#Define variables:
#  . pageCanvas is a boolean to know if we are in an odd page or in a pair page (the canvas is not the same)
#  . mainDict will store all the read informations
#  . indexTag represents the entry in mainDict for a column in the pdf
#  . readIndex (defined later) is the current index of where we are reading the file
pageCanvas = True
mainDict = {}
indexTag = 1

#We will read all pages, and separate all lines, then according to the pageCanvas we have 2 different ways to read the page
for page in pages:
    lines = page.split('\n')
    #print(lines)
    
    #For odd pages, everything start with the entry Patient ID
    #We look for all -20.00 because we have the Length1 and Length2 after that
    #We look for all "something" Sart or "something" End because this is the tag name and we have just after that the angle
    #We look for 27 (franctions) because just after that we have the MU
    #We look for all Y because until an empty string ('') we have all Y values
    #We look for all X1 because until an empty string ('') we have all Y values
    #For X2 it's a little bit more complicated: the first X2 do not correspond to the values, the values are straight after the second Y. For the other X2 it is correct
    #We stored the values for 4 columns by 1 page
    
    if pageCanvas and 'Patient ID:' in lines: #canvas like page 1
        readIndex = 0
        readIndex = lines.index('Patient ID:')
        mainDict["patientId"] = int(lines[readIndex+2])
        for i in range(4):
            mainDict[str(indexTag+i)] = {}
            readIndex = lines[readIndex+4:].index('-20.00') + readIndex+4
            mainDict[str(indexTag+i)]["Length1"] = float(lines[readIndex+2])
            mainDict[str(indexTag+i)]["Length2"] = float(lines[readIndex+3])
            mainDict[str(indexTag+i)]["Y"] = []
            mainDict[str(indexTag+i)]["X1"] = []
            mainDict[str(indexTag+i)]["X2"] = []
        readIndex = lines.index('Patient ID:')
        for i in range(4):
            while readIndex < len(lines) and not ' Start' in lines[readIndex] and not ' End' in lines[readIndex]:
                readIndex += 1
            if readIndex == len(lines):
                break
            mainDict[str(indexTag+i)]["Tag"] = lines[readIndex]
            if lines[readIndex+1] != '':
                mainDict[str(indexTag+i)]["Angle"] = float(lines[readIndex+1])
            else:
                mainDict[str(indexTag+i)]["Angle"] = float(lines[readIndex+2])
            readIndex += 2
        readIndex = lines.index('Patient ID:')
        for i in range(4):
            readIndex = lines[readIndex+2:].index('27') + readIndex+2 +1
            mainDict[str(indexTag +i)]["MU"] = float(lines[readIndex])

        readIndex = lines.index('Patient ID:')
        startX2 = 0
        for i in range(4):
            readIndex = lines[readIndex+2:].index('Y') + readIndex+2 +1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["Y"] += [float(lines[readIndex])]
                readIndex += 1
            if i == 1:
                startX2 = readIndex+1
        readIndex = lines.index('Patient ID:')
        for i in range(4):
            readIndex = lines[readIndex+2:].index('X1') + readIndex+2 +1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["X1"] += [float(lines[readIndex])]
                readIndex += 1
        readIndex = lines.index('Patient ID:')
        for i in range(4):
            readIndex = lines[readIndex+2:].index('X2') + readIndex+2 +1
            if i == 0:
                readIndex = startX2
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["X2"] += [float(lines[readIndex])]
                readIndex += 1
        pageCanvas = not(pageCanvas)
    
    #For pair pages, everything start with the entry Index
    #Y, X1 and X2 are well ordered separated by an empty string (''), so it's easy
    # We just have to read everything one entry by one entry
    
    else: #canvas like page 2
        readIndex = 0
        if not 'Index ' in lines:
            pageCanvas = not(pageCanvas)
            continue
        readIndex = lines.index('Index ')
        readIndex += 2
        while readIndex < len(lines) and lines[readIndex] != '':
            readIndex += 1
        for i in range(4):
            readIndex += 1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag+i)]["Y"] += [float(lines[readIndex])]
                readIndex += 1
            readIndex += 1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag+i)]["X1"] += [float(lines[readIndex])]
                readIndex += 1
            readIndex += 1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag+i)]["X2"] += [float(lines[readIndex])]
                readIndex += 1
        indexTag += 4
        pageCanvas = not(pageCanvas)
print(mainDict)

##Check the vlaues
#Check if for all entries of mainDict, there is a valuable value and 80 values for list
for i in range(len(mainDict)-1):
    if len(mainDict[str(i+1)]["Y"]) != 80:
        print("Y is not correct for " + str(i+1))
        print(Y)
    if len(mainDict[str(i+1)]["X1"]) != 80:
        print("X1 is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["X1"])
    if len(mainDict[str(i+1)]["X2"]) != 80:
        print("X2 is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["X2"])
    if mainDict[str(i+1)]["Tag"] == "":
        print("Tag is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["Tag"])
    if not isinstance(mainDict[str(i+1)]["MU"], float):
        print("MU is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["MU"])
    if not isinstance(mainDict[str(i+1)]["Angle"], float):
        print("Angle is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["Angle"])
    if not isinstance(mainDict[str(i+1)]["Length1"], float):
        print("Length1 is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["Length1"])
    if not isinstance(mainDict[str(i+1)]["Length2"], float):
        print("Length2 is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["Length2"])
if not isinstance(mainDict["patientId"], int):
    print("patientId is not correct")
    print(mainDict["patientId"])
print("Done")

##Write the Excel
#Create the Excel and the sheet, and write the headers
wb = Workbook()
ws = wb.active
ws.title = "Data"
ws['A1'] = "Tag"
ws['A2'] = "Gantry Angle"
ws['A3'] = "Length1(cm) UL"
ws['A4'] = "Length2(cm) UL"
ws['A5'] = "MU"
ws['A6'] = "Y/X1/X2 (mm)"
for row in range(80):
    _ = ws.cell(column=1, row=row+7, value=str(row+1))

#Write for all entries in mainDict
for i in range(len(mainDict)-1):
    _ = ws.cell(column=3*i+2, row=1, value=mainDict[str(i+1)]["Tag"])
    _ = ws.cell(column=3*i+2, row=2, value=mainDict[str(i+1)]["Angle"])
    _ = ws.cell(column=3*i+2, row=3, value=mainDict[str(i+1)]["Length1"])
    _ = ws.cell(column=3*i+2, row=4, value=mainDict[str(i+1)]["Length2"])
    _ = ws.cell(column=3*i+2, row=5, value=mainDict[str(i+1)]["MU"])
    _ = ws.cell(column=3*i+2, row=6, value="Y")
    for row in range(80):
        _ = ws.cell(column=3*i+2, row=row+7, value=str(mainDict[str(i+1)]["Y"][row]))
    _ = ws.cell(column=3*i+3, row=6, value="X1")
    for row in range(80):
        _ = ws.cell(column=3*i+3, row=row+7, value=str(mainDict[str(i+1)]["X1"][row]))
    _ = ws.cell(column=3*i+4, row=6, value="X2")
    for row in range(80):
        _ = ws.cell(column=3*i+4, row=row+7, value=str(mainDict[str(i+1)]["X2"][row]))

#Save the Excel
wb.save(filename = "/Users/tbaudier/guillaume/" + str(mainDict["patientId"]) + "_values.xlsx")
