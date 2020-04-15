import pdfminer.high_level
import openpyxl
from openpyxl import Workbook
import sys
#Read the pdf
text = pdfminer.high_level.extract_text('/Users/tbaudier/guillaume/2004649_Segment.pdf')

##Read the pdf
#Separate all pages
pages = text.split('\x0c')
#print(pages)

#Define variables:
#  . pageCanvas is a boolean to know if we are in an odd page or in a pair page (the canvas is not the same)
#  . mainDict will store all the read informations
#  . indexTag represents the entry in mainDict for a column in the pdf
#  . nbColumn is the number of columns per page (usually 4)
#  . readIndex (defined later) is the current index of where we are reading the file
#  . nbRow (defined later) is the number of rows in the odd page
pageCanvas = True
mainDict = {}
indexTag = 1
nbColumn = 0

#We will read all pages, and separate all lines, then according to the pageCanvas we have 2 different ways to read the page
for page, pageIndex in zip(pages, range(len(pages))):
    lines = page.split('\n')
    #print(lines)
    
    #For odd pages, everything start with the entry Patient ID
    #We look for all -20.00 because we have the Length1 and Length2 after that
    #We look for all "something" Start or "something" End because this is the tag name and we have just after that the angle
    #We look for fractions because just after that we have the MU. Fractions is identical for all pages and for the first page it's just before the first X2 (different place for other pages)
    #We look for the number of rows in the page. To do so, we look for the first index value in the following page -1
    #We look for all Y because until an empty string ('') we have all Y values
    #We look for all X1 because until an empty string ('') we have all Y values
    #For X2 it's a little bit more complicated: the first X2 is not followed by the values. To find the values we look for nbRows float between 2 empty string. For the other X2 it is correct
    #We stored the values for nbColumn (usually 4) columns by 1 page

    if pageCanvas and 'Patient ID:' in lines: #canvas like page 1
        readIndex = 0
        nbRow = 0
        readIndex = lines.index('Patient ID:')
        if not "patientId" in mainDict:
            mainDict["patientId"] = int(lines[readIndex+2])
        if not "fractions" in mainDict:
            readIndex = lines.index('X2')
            mainDict["fractions"] = int(lines[readIndex-2])
        linesSecondPage = pages[pageIndex +1].split('\n')
        readIndexSecondPage = linesSecondPage.index('Index ')
        while readIndexSecondPage < len(linesSecondPage):
            try:
                nbRow = int(linesSecondPage[readIndexSecondPage]) -1
                break
            except:
                readIndexSecondPage += 1
        readIndex = lines.index('Patient ID:')
        nbColumn = 0
        while readIndex < len(lines):
            while readIndex < len(lines) and not ' Start' in lines[readIndex] and not ' End' in lines[readIndex]:
                readIndex += 1
            if readIndex == len(lines):
                break
            mainDict[str(indexTag+nbColumn)] = {}
            mainDict[str(indexTag+nbColumn)]["Tag"] = lines[readIndex]
            if lines[readIndex+1] != '':
                mainDict[str(indexTag+nbColumn)]["Angle"] = float(lines[readIndex+1])
            else:
                mainDict[str(indexTag+nbColumn)]["Angle"] = float(lines[readIndex+2])
            nbColumn += 1
            readIndex += 2
        readIndex = lines.index('Patient ID:')
        for i in range(nbColumn):
            readIndex = lines[readIndex+4:].index('-20.00') + readIndex+4
            mainDict[str(indexTag+i)]["Length1"] = float(lines[readIndex+2])
            mainDict[str(indexTag+i)]["Length2"] = float(lines[readIndex+3])
            mainDict[str(indexTag+i)]["Y"] = []
            mainDict[str(indexTag+i)]["X1"] = []
            mainDict[str(indexTag+i)]["X2"] = []
        readIndex = lines.index('Patient ID:')
        i = 0
        while i<nbColumn:
            readIndex = lines[readIndex+2:].index(str(mainDict["fractions"])) + readIndex+2 +1
            try:
                int(lines[readIndex])
                readIndex = readIndex -1
            except:
                mainDict[str(indexTag +i)]["MU"] = float(lines[readIndex])
                i += 1
        pageCanvas = not(pageCanvas)

        readIndex = lines.index('Patient ID:')
        startX2 = 10000000
        for i in range(nbColumn):
            readIndex = lines[readIndex+2:].index('Y') + readIndex+2 +1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["Y"] += [float(lines[readIndex])]
                readIndex += 1
        readIndex = lines.index('Patient ID:')
        for i in range(nbColumn):
            readIndex = lines[readIndex+2:].index('X1') + readIndex+2 +1
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["X1"] += [float(lines[readIndex])]
                readIndex += 1
        readIndex = lines.index('Patient ID:')
        for i in range(nbColumn):
            readIndex = lines[readIndex+2:].index('X2') + readIndex+2 +1
            if i == 0:
                tempFirstReadIndex = readIndex
                listAllEmpytString = [i+readIndex for i,val in enumerate(lines[readIndex:]) if val==""]
                listAllEmpytString = [0] + listAllEmpytString
                j = 1
                foundX2 = False
                while (j<len(listAllEmpytString) and listAllEmpytString[j] - listAllEmpytString[j-1] -1 != nbRow) or not foundX2:
                    if listAllEmpytString[j] - listAllEmpytString[j-1] -1 == nbRow:
                        try:
                            _ = int(lines[listAllEmpytString[j-1]+1])
                        except:
                            startX2 = listAllEmpytString[j-1]+1
                            break
                    j += 1
                if startX2 == 10000000:
                    print("X2 was not found")
                    sys.exit()
                readIndex = startX2
            while readIndex < len(lines) and lines[readIndex] != '':
                mainDict[str(indexTag +i)]["X2"] += [float(lines[readIndex])]
                readIndex += 1
            if i == 0:
                readIndex = tempFirstReadIndex
    
    #For pair pages, everything start with the entry Index determined before to know the nbRow
    #Y, X1 and X2 are well ordered separated by an empty string (''), so it's easy
    # We just have to read everything one entry by one entry
    # We store nbStrips to check later if it's always the same number (usually 80)
    
    else: #canvas like page 2
        readIndex = 0

        if not 'Index ' in lines:
            indexTag += nbColumn
            pageCanvas = not(pageCanvas)
            continue
        readIndex += readIndexSecondPage
        while readIndex < len(lines) and lines[readIndex] != '':
            readIndex += 1
        if not "nbStrips" in mainDict and readIndex < len(lines) and lines[readIndex] == '':
            mainDict["nbStrips"] = int(lines[readIndex-1])
        for i in range(nbColumn):
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
        indexTag += nbColumn
        pageCanvas = not(pageCanvas)
#print(mainDict)

##Check the vlaues
#Check if for all entries of mainDict, the type of the value is correct type and there is nbStrip (usually 80) values for list

if not isinstance(mainDict["nbStrips"], int):
    print("nbStrips is not correct")
    print(mainDict["nbStrips"])
if mainDict["nbStrips"] != 80:
    print("nbStrips is not equal to 80")
    print(mainDict["nbStrips"])
for i in range(len(mainDict)-3):
    if mainDict[str(i+1)]["Tag"] == "":
        print("Tag is not correct for " + str(i+1))
        print(mainDict[str(i+1)]["Tag"])
    if len(mainDict[str(i+1)]["Y"]) != mainDict["nbStrips"]:
        print("Y is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["Y"])
    if len(mainDict[str(i+1)]["X1"]) != mainDict["nbStrips"]:
        print("X1 is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["X1"])
    if len(mainDict[str(i+1)]["X2"]) != mainDict["nbStrips"]:
        print("X2 is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["X2"])
    if not isinstance(mainDict[str(i+1)]["MU"], float):
        print("MU is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["MU"])
    if not isinstance(mainDict[str(i+1)]["Angle"], float):
        print("Angle is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["Angle"])
    if not isinstance(mainDict[str(i+1)]["Length1"], float):
        print("Length1 is not correct for " + mainDict[str(i+1)]["Tag"])
        print(mainDict[str(i+1)]["Length1"])
    if not isinstance(mainDict[str(i+1)]["Length2"], float):
        print("Length2 is not correct for " + mainDict[str(i+1)]["Tag"])
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
for i in range(len(mainDict)-3):
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
