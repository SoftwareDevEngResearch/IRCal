# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:46:19 2018
@author: capland
modified by Derek Bean
"""

import pandas as pd
import numpy as np
import h5py
import os
import glob



class Convert_sf():
    def __init__(self, opendir, savedir, fname):
        self.opendir = opendir.replace('\\', '/')
        if self.opendir[0] == '/':
            self.opendir = '/' + opendir
        self.savedir = savedir.replace('\\', '/')
        if self.savedir[0] == '/':
            self.savedir = '/' + savedir
        self.file = fname  # includes the .sf--- suffix

    def scrape_inc(self):  # Get framerate and integration time from .inc file:
        with open(self.opendir+'/'+self.file[:-6] + ".inc", 'r') as f:
            # [:-6] removes the '.sf---' allowing for '.inc' to be appended
            inc = f.read().split()
            framerate_index = inc.index('FRate_0') + 1
            IntTime_index = inc.index('ITime_0') + 1
            self.framerate = float(inc[framerate_index])
            self.int_time = float(inc[IntTime_index])
        return self.framerate, self.int_time

    def imread(self):  # Read in the video/image data:
        with open(self.opendir+'/'+self.file, 'r') as f:
            # Skip the text header and find the beginning of the binary data:
            content = f.read()

            # scrape the metadata in the sf file:
            self.width = int(content.split()
                             [content.split().index('xPixls')+1])

            self.height = int(content.split()
                              [content.split().index('yPixls')+1])

            # Number of frames the sf file claims (could be different than
            # the actual number if the camera dropped frames):
            frames_claimed = int(content.split()
                                 [content.split().index('NumDPs')+1])

            f.seek(content.index('DATA')+75, os.SEEK_SET)
            # 75 is length of 'DATA' plus carriage return

            del content  # clear the content variable from memory

            # Load the binary data into a 1D array:
            self.data = np.fromfile(f, dtype=np.uint16)
            # Reshape into a 3D matrix of nframes(auto), height, width:
            self.data = np.reshape(self.data, (-1, self.height, self.width))

            self.nframes = self.data.shape[0]  # Actual number of frames
            self.drop = frames_claimed - self.nframes

        return self.data, self.width, self.height, self.nframes, self.drop

    def convert(self):
        self.imread()
        self.scrape_inc()
        if not os.path.exists(self.savedir):
            os.makedirs(self.savedir)
        with h5py.File(self.savedir+'/'+self.file[:-6] + ".hdf5", 'w') as f:
            f.create_dataset('data', data=self.data)
            f.create_dataset('nframes', data=self.nframes)
            f.create_dataset('width', data=self.width)
            f.create_dataset('height', data=self.height)
            f.create_dataset('drop', data=self.drop)
            f.create_dataset('framerate', data=self.framerate)
            f.create_dataset('int_time', data=self.int_time)
        return self.data

    def convert_batch(self, opendir, savedir):
        os.chdir(opendir)
        [self.Convert_sf(opendir, savedir, file).convert() for file in glob.glob('*.sfmof')]


def add_conditions(condfile, datadir):
    datadir = datadir.replace('\\', '/')
    if datadir[0] == '/':
        datadir = '/' + datadir
    condfile = condfile.replace('\\', '/')
    if condfile[0] == '/':
        condfile = '/' + condfile

    files = os.listdir(datadir)
    conditions = pd.read_csv(condfile, sep='\t')
    variables = list(conditions)  # list of test condition variables
    for x in files:
        try:
            # row is hard coded with 'DP-', and 2 digits at before '.hdf5':
            row = conditions.loc[conditions['DP-'] ==
                                 float(x[:-5][-2:])].index[0]
        except IndexError:
            print 'Warning: no test conditions for', x
        with h5py.File(datadir+'/'+x, 'r+') as f:
            for y in variables:
                try:
                    f.create_dataset(y, data=conditions.loc[row][y])
                except RuntimeError:
                    print 'Skipped adding', y, 'to', x,\
                        'because it already exists.'


if __name__ == '__main__':
    OpenDir = 'D:\Kernel IR Data\PythonProject\CameraData'
    SaveDir = 'D:\Kernel IR Data\PythonProject\ConvertedData'
    conditionsfile = 'D:\Kernel IR Data\PythonProject\TestConditions.txt'

    print 'Converting sfmov files to hdf5...'
    convert_batch(OpenDir, SaveDir)

    print 'Adding test conditions to hdf5 files...'
    add_conditions(conditionsfile, SaveDir)