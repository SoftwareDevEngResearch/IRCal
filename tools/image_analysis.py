# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python script for conducting image analysis on infrared images
@author: Derek Bean
"""

import h5py
import os


class Image_Tools():
    def __init__(self, file_path, file_name):
        self.file_path = self.path_handling(file_path)
        self.file_name = file_name
        self.data_attributes = {}

    @staticmethod
    def path_handling(path):
        """ TODO: Need to remove and replace function with os package for path handling across operating systems"""
        path.replace('\\', '/')
        if path[0] == '/':
            path = '/' + path
        return path


    def open_hdf5(self):
        """
        Open and return a file object based on the input path

        Input:
        extension: a string with the
        """
        return h5py.File(os.path.join(self.file_path, self.file_name + '.hdf5'), 'r')

    def get_attributes(self):
        """
        Get the values for important parameters from the hdf5 file such as dropped frames and the frame rate

        :returns a dictionary of the important attributes with the keys the same as those in the hdf5 file
        """
        data = {}
        with self.open_hdf5() as file:
            for key in file.keys():
                if 'data' not in key.lower():
                    data[key] = file.get(key)[()]
        self.data_attributes = data
        return self.data_attributes

    def read_frames(self, frame_number=-1):
        try:
            number_of_frames = self.data_attributes['number_of_frames']
        except NameError:
            self.get_attributes()
            self.read_frames(self, frame_number=frame_number)
        with self.open_hdf5() as file:
            frame_dataset = file.get('data')[()]
            print(frame_dataset)
        return frame_dataset

    def img_rms(self):
        return None

    def define_roi(self):
        return None

    def background_subratction(self):
        return None