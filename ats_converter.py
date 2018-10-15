# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:46:19 2018
@author: caplanda
modified by Derek Bean
"""


import os

if __name__ == '__main__':

    filePath = 'D:\Ignition_10_12_2018'
    fileName = 'Rec-000003.ats'

    totalPath = os.path.join(filePath, fileName)
    fileContents = []
    with open(totalPath, 'rb') as atsFile:
        for row in atsFile:
            rowContents = row.strip(b'\n').strip(b'\r').split(b' ')
            fileContents.append(rowContents)
