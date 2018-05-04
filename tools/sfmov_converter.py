# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:46:19 2018
@author: capland
modified by Derek Bean
"""

import numpy as np
import h5py
import os


class SfmovTools:
    def __init__(self, opendir, savedir, fname):
        self.opendir = self.path_handling(opendir)
        self.savedir = self.path_handling(savedir)
        self.file = fname  # includes the .sf--- suffix

    @staticmethod
    def path_handling(path):
        path.replace('\\', '/')
        if path[0] == '/':
            path = '/' + path
        return path

    def scrape_inc(self):  # Get framerate and integration time from .inc file:
        with open(self.opendir+'/'+self.file[:-6] + ".inc", 'r') as f:
            # [:-6] removes the '.sf---' allowing for '.inc' to be appended
            inc = f.read().split()
            framerate_index = inc.index('FRate_0') + 1
            int_time_index = inc.index('ITime_0') + 1
            self.framerate = float(inc[framerate_index])
            self.int_time = float(inc[int_time_index])
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
            self.dropped_frames = frames_claimed - self.nframes

        return self.data, self.width, self.height, self.nframes, self.dropped_frames

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
            f.create_dataset('drop', data=self.dropped_frames)
            f.create_dataset('framerate', data=self.framerate)
            f.create_dataset('int_time', data=self.int_time)
        return self.data
