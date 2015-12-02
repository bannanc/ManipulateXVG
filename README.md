# ManipulateXVG
cleaning, combining and extracting data from xvg files (output from gromacs)

We recently ran into an issue where we wanted to combine xvg output with different start/end times, this address our current problem. 
It inlcudes a method "removeCorreuptLines" which removes any line from the "data" section of the xvg file that cannot be read in as floats.

There are three methods in the fixXVG.py script that can be imported:

######findDataStart(lines) 
This takes a list of lines and finds the first one that is data (can be read as a float)

######removeCorruptLines(inputFN, outputFN = None) 
This takes in an xvg file and removes any corrupted lines. If an output file name is provided it writes the fixed version there, if an output is not provided then the fixed version will be written to a file of the same name as the input. 

######CombineXVG(input1, input2, output)
This takes in two input xvg files and adds the data from the second to the first one, it removes any times at the beginning of the second output that are smaller than the last time in the first input the results are written to the output file. This uses the removeCorruptLines so no "bad" lines should be written to the output file. 
