# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:46:19 2018
@author: caplanda
modified by Derek Bean
"""


import os
import numpy as np

def decode_string(string):
    try:
        outputString = position.decode('ascii')
    except UnicodeDecodeError:
        outputString = np.fromiter(position, dtype=np.double)
    return outputString



if __name__ == '__main__':

    filePath = 'D:\Ignition_10_12_2018'
    fileName = 'test_001.cine'

    totalPath = os.path.join(filePath, fileName)
    fileContents = []
    with open(totalPath, 'rb') as atsFile:
        for row in atsFile:
            rowContents = row.strip(b'\n').strip(b'\r').split(b' ')
            tempStrings = []
            for position in rowContents:
                tempStrings.append(decode_string(position))

            fileContents.append(tempStrings)
