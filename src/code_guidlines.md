GraphProgram
============

Directory structure:

This directory (src) contains all of the code for the Graph Program.
Code for the underlying python graph library lives in graphlib directory which defines the graphlib package. This is the reason that the src directory should be in your pythonpath, so that python knows about the graphlib package.
Any code using the graphlib package to tackle a specific problem should be located in the scripts directory, within a subdirectory for that specific problem, e.g. scripts for the radio-k labeling problem from fall of 2015 would be in the scripts/radio_fall_2015 directory.
Finally, code for the GUI application available for figure generation and computations for those who do not want to write python scripts directly is located in the app directory. This code is currently in transition from a python app with a tkinter frontend to a d3 frontend with Flask backend. 

Code Conventions:

Python:
Standard python naming conventions (mostly) apply: 
 - underscore_case variables, attributes, functions and methods
 - TitleCase classes
 - Capital letters are allowed for vectors and matrices
Document using """docstrings""", provide inline comments with standard #comment syntax as necessary. Document all source files with when the file originated, who the authors are, and a description of what the file is for. Document classes with a high-level description, and a list with one-line description of all public class methods, attributes, and object methods. Document functions and methods with a brief description (omit if return value tells everything), a list and one-line description of all parameters (leaving out self or cls is acceptable), and a description of the return value.