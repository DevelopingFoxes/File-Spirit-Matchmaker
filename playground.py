# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:40:02 2024

@author: _
"""

# === IMPORTS ===

from pathlib import Path
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())

# === ===


### === PLAY GROUND ===

var = input("Directory Path to Scan: ")

print('Exist: ' ,Path(var).exists())
print('Is File: ', Path(var).is_file())
print('Is Dir: ',Path(var).is_dir())


file2 = input("fileTwo: ")
print('Exist: ' ,Path(file2).exists())
print('Is File: ', Path(file2).is_file())
print('Is Dir: ',Path(file2).is_dir())
print('')
print ('Same-File: ', Path(var).samefile(Path(file2)))



### === NOTES ===

''' # Gets file name (incl. ext)
PurePosixPath('my/library/setup.py').name
'''

''' # Gets file extention
PurePosixPath('my/library/setup.py').suffix

'''

''' # Gets filename w/o ext.
PurePosixPath('my/library.tar').stem
>'library'
'''