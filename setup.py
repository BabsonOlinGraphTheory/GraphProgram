"""
This script uses py2exe to create a windows executable version of the program. Works with python 3.4 as of 2/10/2015

Babson/Olin Graph Research Spring 2015
Josh Langowitz
"""
from distutils.core import setup
import py2exe

windows = {
	'script':'graphProgram.py'
}
opts = {
    'py2exe': {
        'includes': [
            'Gui',
            'generate',
            'graphmath',
            'labeler',
            'labeling',
            'graph',
            'view'
        ],
        'optimize' : 2
        }
}
setup(windows=[windows], options=opts)