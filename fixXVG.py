import os
import os
import numpy as np
import commands as c

def findDataStart(lines, delin = ' '):
    """
    Finds the line where the data starts

    input:
        lines = list of strings (probably from a data file)
        delin = optional string, tells how the data would be separated, default is a space (' ')
    
    output:
        i = integer where the data stops being a string (returns -1 if no data was found)
        header = lines that make up the strings at the top of the file
        datalines = lines starting from where the data ends
    """
    
    for i, l in enumerate(lines):
        test = l.split(delin)[0]
        # If it can't be turned into a float is is still a part of the header
        try:
            float(test)
            return i, lines[0:i], lines[i:]
        except:
            continue
    return -1, lines, []

def removeCorruptLines(inputFN, outputFN = 'output.xvg', headerLine = None, warn = 10.0, fail = 20.0):
    """
    This method takes an .xvg file, removes any corrupted lines of data or data lines that are not sufficiently long. 

    input:
        inputFN - (String) name of input file
        outputFN - (optional string) name of output file, default is output.xvg, you can provide the same name as the input file, but it will be over written. 
        outputFN - (optional, String) name of outputfile, will out output a file with the same name as input if not provided
        headerLine - (optional, int) number of lines at the beginning of the file consisting of strings, if None this will be found, if you know there is no header assign header = 0.
        warn - (optional, float) the percent of data that can be removed before a warning is printed. 
        failing - (optional, float) the percent of data that can be removed and still run the program. If more data is run an exception is raised. 

    output:
        no returns, but creates an output file with all of the non-corrupt data from the input file. 
    """

    # If input file not found raise an exception
    if not os.path.isfile(inputFN):
        fileError = Exception("Input File not found!")
        raise fileError
    
    # Read in file to find header and length of data
    inputFile = open(inputFN,'r')
    lines = inputFile.readlines()
    inputFile.close()

    # Need header lines for numpy.genfromtxt to work
    # If not provided find it:
    if headerLine == None:
        headerLine, header, datalines = findDataStart(lines)
        # Turn list of lines in header into a single string
        header = ''.join(header)

    # If headerLine was provided and it's bigger than zero get header:
    elif headerLine > 0:
        header = lines[0:headerLine]
        # Make header lines into string
        header = ''.join(header)

    else: # headerLine == 0:
        header = '' # This is default for numpy.savetxt

    # For writing header purposes we do not want the last character to create new line
    if header[-1] == '\n':
        header = header[:-1]

    # length of original data set:
    dataLength = len(lines) - headerLine

    # Use genfromtxt to get data
    # skip_header skips lines at the beginning of the file
    # invalid_raise means that if a line is found with the wrong number of entries then it will be ignored and a warning will be printed
    data = np.genfromtxt(inputFN, skip_header = headerLine, invalid_raise = False)
    
    # Percent of data removed:
    difLength = dataLength - len(data)
    warning = int(warn * dataLength)
    failing = int(fail * dataLength)

    if difLength == 0:
        print "No corrupt lines found, no data was removed"
    elif difLength >= failing:
        lenthError = Exception("%i corrupted lines found, that is more than %.1f percent. Removal failed, you should examin your input files" % (difLength, fail))
        raise lengthError
    elif difLength >= warning:
        print "WARNING: warning %i corrupted lines found and removed, which is more than the warning limit %.1f percent" % (difLength, warn)
    else: # Lines removed, but less than warning limit
        print "%i corrupt lines found and removed" % difLength


    # Use numpy savetxt to write data (with header) to the output file
    # fmt assigns the format of the float, for now it is the longest decimal in examples considered
    # header prints the header from the original file to the top of the output
    # comments adds that character to the beginning of ever line in the header
    np.savetxt(outputFN, data, fmt='%.10f', header = header, comments = '')

    print "file %s created with corrected data" % outputFN 
   


# CombineXVG takes in two xvg files and combines data from the second one at the end of the first one starting at the last time in the first file
def CombineXVG(input1, input2, output):
    """
    This method takes in two input .xvg files and adds the data from the second to the end of the first

    input:
        input1: first input file string.xvg
        input2: data you want to add to the end of the first input
        output: name of file for the combined data
    
    output:
        returns lines that were written to output file
        creates output file with combined data
    """
    fix1 = input1.split('.')[0]+'_fixed.xvg'
    fix2 = input2.split('.')[0]+'_fixed.xvg'
    # clean up the input files
    removeCorruptLines(input1, outputFN = fix1)
    removeCorruptLines(input2, outputFN = fix2)

    # Read in lines and close file
    f1 = open(fix1)
    f2 = open(fix2)
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    f1.close()
    f2.close()

    # find where the data starts for both of them
    end1, header1, dataLines1 = findDataStart(lines1)
    end2, header2, dataLines2 = findDataStart(lines2)

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
            concat = False

    # combine data
    if concat:
        outputLines = lines1 + dataLines2[i:]
        print "Files combined and written to ",output
    else:
        outputLines = lines1
        print "No new data foudn in second input file"

    # write output file
    outFile = open(output,'w')
    outFile.writelines(outputLines)
    outFile.close()
    return outputLines
    
import numpy as np
import commands as c

def findDataStart(lines, delin = ' '):
    """
    Finds the line where the data starts

    input:
        lines = list of strings (probably from a data file)
        delin = optional string, tells how the data would be separated, default is a space (' ')
    
    output:
        i = integer where the data stops being a string (returns -1 if no data was found)
        header = lines that make up the strings at the top of the file
        datalines = lines starting from where the data ends
    """
    
    for i, l in enumerate(lines):
        test = l.split(delin)[0]
        # If it can't be turned into a float is is still a part of the header
        try:
            float(test)
            return i, lines[0:i], lines[i:]
        except:
            continue
    return -1, lines, []

def removeCorruptLines(inputFN, outputFN = 'output.xvg', headerLine = None, warning = 10.0, failing = 20.0):
    """
    This method takes an .xvg file, removes any corrupted lines of data or data lines that are not sufficiently long. 

    input:
        inputFN - (String) name of input file
        outputFN - (optional string) name of output file, default is output.xvg, you can provide the same name as the input file, but it will be over written. 
        outputFN - (optional, String) name of outputfile, will out output a file with the same name as input if not provided
        headerLine - (optional, int) number of lines at the beginning of the file consisting of strings, if None this will be found, if you know there is no header assign header = 0.
        warning - (optional, float) the percent of data that can be removed before a warning is printed. 
        failing - (optional, float) the percent of data that can be removed and still run the program. If more data is run an exception is raised. 

    output:
        no returns, but creates an output file with all of the non-corrupt data from the input file. 
    """

    # If input file not found raise an exception
    if not os.path.isfile(inputFN):
        fileError = Exception("Input File not found!")
        raise fileError
    
    # Read in file to find header and length of data
    inputFile = open(inputFN,'r')
    lines = inputFile.readlines()
    inputFile.close()

    # Need header lines for numpy.genfromtxt to work
    # If not provided find it:
    if headerLine == None:
        headerLine, header, datalines = findDataStart(lines)
        # Turn list of lines in header into a single string
        header = ''.join(header)

    # If headerLine was provided and it's bigger than zero get header:
    elif headerLine > 0:
        header = lines[0:headerLine]
        # Make header lines into string
        header = ''.join(header)

    else: # headerLine == 0:
        header = '' # This is default for numpy.savetxt

    # For writing header purposes we do not want the last character to create new line
    if header[-1] == '\n':
        header = header[:-1]

    # length of original data set:
    dataLength = len(lines) - headerLine

    # Use genfromtxt to get data
    # skip_header skips lines at the beginning of the file
    # invalid_raise means that if a line is found with the wrong number of entries then it will be ignored and a warning will be printed
    data = np.genfromtxt(inputFN, skip_header = headerLine, invalid_raise = False)
    
    # Percent of data removed:
    difLength = dataLength - len(data)
    warning = int(warn * dataLength)
    failing = int(fail * dataLength)

    if difLength == 0:
        print "No corrupt lines found, no data was removed"
    elif difLength >= failing:
        lenthError = Exception("%i corrupted lines found, that is more than %.1f percent. Removal failed, you should examin your input files" % (difLength, fail))
        raise lengthError
    elif difLength >= warning:
        print "WARNING: warning %i corrupted lines found and removed, which is more than the warning limit %.1f percent" % (difLength, warn)
    else: # Lines removed, but less than warning limit
        print "%i corrupt lines found and removed" % difLength


    # Use numpy savetxt to write data (with header) to the output file
    # fmt assigns the format of the float, for now it is the longest decimal in examples considered
    # header prints the header from the original file to the top of the output
    # comments adds that character to the beginning of ever line in the header
    np.savetxt(outputFN, data, fmt='%.10f', header = header, comments = '')

    print "file %s created with corrected data" % outputFN 
   


# CombineXVG takes in two xvg files and combines data from the second one at the end of the first one starting at the last time in the first file
def CombineXVG(input1, input2, output):
    """
    This method takes in two input .xvg files and adds the data from the second to the end of the first

    input:
        input1: first input file string.xvg
        input2: data you want to add to the end of the first input
        output: name of file for the combined data
    
    output:
        returns lines that were written to output file
        creates output file with combined data
    """
    fix1 = input1.split('.')[0]+'_fixed.xvg'
    fix2 = input2.split('.')[0]+'_fixed.xvg'
    # clean up the input files
    removeCorruptLines(input1, outputFN = fix1)
    removeCorruptLines(input2, outputFN = fix2)

    # Read in lines and close file
    f1 = open(fix1)
    f2 = open(fix2)
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    f1.close()
    f2.close()

    # find where the data starts for both of them
    end1, header1, dataLines1 = findDataStart(lines1)
    end2, header2, dataLines2 = findDataStart(lines2)

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
            concat = False

    # combine data
    if concat:
        outputLines = lines1 + dataLines2[i:]
        print "Files combined and written to ",output
    else:
        outputLines = lines1
        print "No new data foudn in second input file"

    # write output file
    outFile = open(output,'w')
    outFile.writelines(outputLines)
    outFile.close()
    return outputLines
    
