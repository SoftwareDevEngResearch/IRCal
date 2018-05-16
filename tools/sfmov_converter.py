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
        self.file = os.path.splitext(os.path.basename(fname))[0]
        self.frame_rate = float
        self.int_time = float
        self.data = float
        self.dimensions = {'height': int, 'width': int}
        self.number_of_frames = int
        self.dropped_frames = int
        self.length_DATA = 75  # Length of the data in each row with the return character
        self.camera_name = str()

    @staticmethod
    def path_handling(path):
        """ Need to remove and replace function with os package"""
        path.replace('\\', '/')
        if path[0] == '/':
            path = '/' + path
        return path

    @staticmethod
    def extensions():
        """Returns the file extension that are used in the class"""
        return {'sfmov': '.sfmov', 'inc': '.inc', 'hdf5': '.hdf5'}

    def open_file(self, extension):
        """ Open and return a file object based on the input path"""
        return open(os.path.join(self.opendir, self.file + self.extensions()[extension]),
                    'r+b')

    def scrape_inc(self):
        """Scrape the integration time and frame rate from the .inc file and store
        them as object variables"""
        with self.open_file('inc') as file:
            file_lines = file.readlines()
            inc_data = {x[0]: x[1:] for x in [s.split(b' ') for s in file_lines]}
            print(inc_data.keys())
            self.int_time = float(inc_data[b'ITime_0'][0])
            self.frame_rate = float(inc_data[b'FRate_0'][0])
            self.camera_name = inc_data[b'xmrCameraName'][0].strip(b'\n')
        return self.frame_rate, self.int_time, self.camera_name

    def imread(self):
        """ Read the images from the object filepath"""
        with self.open_file('sfmov') as file:
            # Skip the text header and find the beginning of the binary data:

            # rows = (row.split() for row in f.read().split(b'\n'))
            content = {}
            for row in file:
                row_contents = row.strip(b'\n').strip(b'\r').split(b' ')
                content[row_contents[0]] = row_contents[1:]
                if b'DATA' in row:
                    break
            self.data = np.fromfile(file, dtype=np.uint16)
            # scrape the metadata in the sf file:
            self.dimensions['width'] = int(content.pop(b'xPixls')[0])

            self.dimensions['height'] = int(content.pop(b'yPixls')[0])

            # Number of frames the sf file claims (could be different than
            # the actual number if the camera dropped frames):
            frames_claimed = int(content.pop(b'NumDPs')[0])
            # Load the binary data into a 1D array:
            self.data = np.reshape(self.data, (-1, self.dimensions['height'], self.dimensions['width']))
            # Reshape into a 3D matrix of nframes(auto), height, width:
            self.number_of_frames = self.data.shape[0]  # Actual number of frames
            self.dropped_frames = frames_claimed - self.number_of_frames
        return self.data, self.dimensions, self.number_of_frames, self.dropped_frames

    def convert(self):
        self.imread()
        self.scrape_inc()
        try:
            with h5py.File(os.path.join(self.savedir, self.file + self.extensions()['hdf5']), 'w-') as file:
                file.create_dataset('data', data=self.data)
                file.create_dataset('number_of_frames', data=self.number_of_frames)
                file.create_dataset('width', data=self.dimensions['width'])
                file.create_dataset('height', data=self.dimensions['height'])
                file.create_dataset('dropped_frames', data=self.dropped_frames)
                file.create_dataset('frame_rate', data=self.frame_rate)
                file.create_dataset('int_time', data=self.int_time)
        except OSError:
            raise OSError('The file already exists please choose a different one or delete the file')
        return self.data
