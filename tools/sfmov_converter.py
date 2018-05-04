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
        self.file = fname.replace('.sfmov', '')  # includes the .sf--- suffix
        self.extensions = {'sfmov': '.sfmov', 'inc': '.inc'}
        self.framerate = None
        self.int_time = None
        self.data = None
        self.dimensions = {'height': int, 'width': int}
        self.number_of_frames = int
        self.dropped_frames = int

    @staticmethod
    def path_handling(path):
        path.replace('\\', '/')
        if path[0] == '/':
            path = '/' + path
        return path

    def open_file(self, extension):
        return open(os.path.join(self.opendir, self.file, self.extensions[extension]), 'r')

    def scrape_inc(self):  # Get framerate and integration time from .inc file:
        with self.open_file('.inc') as f:
            # [:-6] removes the '.sf---' allowing for '.inc' to be appended
            inc = f.read().split()
            framerate_index = inc.index('FRate_0') + 1
            int_time_index = inc.index('ITime_0') + 1
            self.framerate = float(inc[framerate_index])
            self.int_time = float(inc[int_time_index])
        return self.framerate, self.int_time

    def imread(self):  # Read in the video/image data:
        with self.open_file('.sfmov') as f:
            # Skip the text header and find the beginning of the binary data:
            content = f.read()

            # scrape the metadata in the sf file:
            self.dimensions['width'] = int(content.split()
                                       [content.split().index('xPixls')+1])

            self.dimensions['height'] = int(content.split()
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
            self.data = np.reshape(self.data, (-1, self.dimensions['height'], self.dimensions['width']))

            self.number_of_frames = self.data.shape[0]  # Actual number of frames
            self.dropped_frames = frames_claimed - self.number_of_frames

        return self.data, self.dimensions, self.number_of_frames, self.dropped_frames

    def convert(self):
        self.imread()
        self.scrape_inc()
        if not os.path.exists(self.savedir):
            os.makedirs(self.savedir)
        with h5py.File(self.savedir+'/'+self.file[:-6] + ".hdf5", 'w') as f:
            f.create_dataset('data', data=self.data)
            f.create_dataset('nframes', data=self.number_of_frames)
            f.create_dataset('width', data=self.dimensions['width'])
            f.create_dataset('height', data=self.dimensions['height'])
            f.create_dataset('drop', data=self.dropped_frames)
            f.create_dataset('framerate', data=self.framerate)
            f.create_dataset('int_time', data=self.int_time)
        return self.data
