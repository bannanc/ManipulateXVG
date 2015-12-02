# ManipulateXVG
cleaning, combining and extracting data from xvg files (output from gromacs)

We recently ran into an issue where we wanted to combine xvg output with different start/end times, this address our current problem. 
It inlcudes a method "removeCorreuptLines" which removes any line from the "data" section of the xvg file that cannot be read in as floats.

