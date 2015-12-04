import os
import commands as c

def findDataStart(lines):
    """
    Finds the line where the data starts

    input:
        lines = list of strings (probably from a data file)
        delin = optional string, tells how the data would be separated
    
    output:
        i = integer where the data stops being a string

    """
    
    for i, l in enumerate(lines, delin = ' '):
        test = l.split(' ')[0]
        # If it can't be turned into a float is is still a part of the header
        try:
            float(test)
            return i, lines[i:]
        except:
            continue
    return -1, []

def removeCorruptLines(inputFN, outputFN = None, header = None, comments = ['#','@']):
    """
    This method takes an .xvg file, removes any corrupted lines of data or data lines that are not sufficiently long. 

    input:
        inputFN - (String) name of input file
        outputFN - (optional, String) name of outputfile, will out output a file with the same name as input if not provided
        header - (optional, int) number of lines at the beginning of the file consisting of strings, if None this will be found, if you know there is no header assign header = 0.
        comments = (optional, list of strings) characters that are used to indicate a comment in your file, default is '#' and '@' which are used in GROMACS xvg file headers. 

    output:
        no returns, but creates an output file with all of the non-corrupt data from the input file. 
    """

    # If input file not found raise an exception
    if not os.path.isfile(inputFN):
        fileError = Exception("Input File not found!")
        raise fileError
    
    # If no output file name assigned, assign output to input file name
    if outputFN == None:
        outputFN = inputFN

    # If you can read in file using np.loadtxt with comments then there is nothing wrong with the file.
    try:
        np.loadtxt(inputFN,comments = comments)
        commands.getoutput('cp %s %s' % (inputFN outputFN))
        print "Input File safe from corruption"
        return 
    except:
        print "At least one line in inputfile needs to be removed"

    # May not need this, researching numpy
    if header == None:
        inputFile = open(inputFN, 'r')
        header, datalines = findDataStart(inputFile.readlines())
        inputFile.close()

     
def removeCorruptLines_original(inputFN, outputFN = None):
    """
        Original version of this method, not removing until I'm convinced the new one works. 
    """
    if outputFN == None:
        outputFN = inputFN
    try:
        inputFile = open(inputFN, 'r')
    except:
        fileError = Exception("Input File not found!")
        raise fileError

    # read in lines from file
    allLines = inputFile.readlines()
    inputFile.close()

    # Find where the data starts
    end, dataLines = findDataStart(allLines)
    newlines = allLines[0:end]
    
    length = len(dataLines[0].split(' '))
    # In each line:
    for l in dataLines:
        goodLine = True
        dataSet = l.split(' ')
        # if the length is not the same then it is not a good line
        if len(dataSet) != length:
            goodLine = False
        else:    
            # for each item, if it can't be turned into a float remove that line
            for s in l.split(' '):
                try:
                    float(s)
                except:
                    goodLine = False
                    break 
        if goodLine:
            newlines.append(l)
    
    # write good lines to output file
    newFile = open(outputFN,'w')
    newFile.writelines(newlines)
    newFile.close()

    return newlines

# CombineXVG takes in two xvg files and combines data from the second one at the end of the first one starting at the last time in the first file
def CombineXVG(input1, input2, output):
    # clean up the input files
    lines1 = removeCorruptLines_original(input1,'temp.xvg')
    lines2 = removeCorruptLines_original(input2,'temp.xvg')

    # find where the data starts for both of them
    end1, dataLines1 = findDataStart(lines1)
    end2, dataLines2 = findDataStart(lines2)

    # time in ps that the first set of data ends
    endTime = float(dataLines1[-1].split(' ')[0])
    i = 0
    # time in ps that the second set of data starts
    startTime = float(dataLines2[i].split(' ')[0])
    concat = True
    # Find the line where the second set of data has a time that is larger than the end of the first set
    while startTime <= endTime and concat:
        i += 1
        # try so that if you get to the end of the second file it doesn't throw an error
        try:
            startTime = float(datalines2[i].split(' ')[0])
        except:
            print "No new data found in second input file"
            concat = False

    # combine data
    if concat:
        outputLines = lines1 + dataLines2[i:]
    else:
        outputLines = lines1

    # write output file
    outFile = open(output,'w')
    outFile.writelines(outputLines)
    outFile.close()
    return outputLines
    
