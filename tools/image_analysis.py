# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python script for conducting image analysis on infrared images
@author: Derek Bean
"""

import os
import tables as tb
import numpy as np
from matplotlib.widgets import EllipseSelector
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import itertools as it

class Image_Tools():
    def __init__(self, file_path, file_name):
        self.file_path = self.path_handling(file_path)
        self.file_name = file_name
        self.data_attributes = {}
        self.get_attributes()

    @staticmethod
    def path_handling(path):
        """ TODO: Need to remove and replace function with os package for path handling across operating systems"""
        path.replace('\\', '/')
        if path[0] == '/':
            path = '/' + path
        return path
    @staticmethod
    def nearest_pixel(value):
        if type(value) == int:
            return value
        elif type(value) == float:
            return int(round(value))
        else:
            try:
                return [int(round(x)) for x in value]
            except TypeError:
                try:
                    return value.round()
                except AttributeError:
                    raise TypeError('The input value is not an int, float, list tuple, dict or numpy array of ints or floats')



    def open_hdf5(self):
        """
        Open and return a file object based on the input path

        Input:
        extension: a string with the
        """
        return tb.open_file(os.path.join(self.file_path, self.file_name + '.hdf5'), 'r')

    def get_attributes(self):
        """
        Get the values for important parameters from the hdf5 file such as dropped frames and the frame rate

        :returns a dictionary of the important attributes with the keys the same as those in the hdf5 file
        """
        data = {}
        with self.open_hdf5() as file:
            for dataset in file.root:
                if 'data' not in dataset.name:
                    data[dataset.name] = dataset.read()
        self.data_attributes = data
        return self.data_attributes

    def read_frames(self, frame_number=-1):
        """

        :param frame_number: desired frames to pull in. defaults to all frames (-1). Can use slice like notation
                             in a string format ie frame_number='0:2' returns the first and second frame
        :return: returns a numpy ndarray of the data
        """
        try:  # Check to see if the file info has been loaded if not load the file data
            self.data_attributes['number_of_frames']
        except KeyError:
            self.get_attributes()
            self.read_frames(self, frame_number)
        with self.open_hdf5() as file:  # Ra=ead the frames from the hdf5 file based on the frame number input
            if frame_number == -1:  # Read all of the frames
                frame_dataset = file.root.data.read()
            else:
                # Handle the string notation format of the frame slices to get the start and stop points
                if type(frame_number) == str:
                    start = int(frame_number.split(':')[0])
                    stop = int(frame_number.split(':')[-1])
                elif type(frame_number) == int:
                    start = frame_number
                    stop = frame_number + 1
                frame_dataset = file.root.data.read(start, stop)

        return frame_dataset

    def show_image(self, frame_number):
        """
        Display desired images from the file in a popup window. Can display multiple images in sequence

        Input:
            frame_number: desired frame number to show. can also use slice like notation encapsulated in a string
                            for example frames 0 and 1 could both be displayed with the input '0:2'. Also accepts ints
        """
        image = self.read_frames(frame_number)
        for frame in range(np.shape(image)[0]):
            plt.imshow(image[frame, :, :])
            plt.show()

    def img_std(self, single_image):
        """
        Return the standard deviation of the input image
        :param:
            single_image: a 2d numpy ndarray
        :return:
            Value of the standard deviation of the image
        TODO: The functionality of this function may need to be changed if a class for images is added
        """
        return np.std(single_image)

    def sequence_average(self, frames):
        return np.ndarray.mean((self.read_frames(frames)))

    def define_roi(self, frame_number=0):
        if type(frame_number) != int:
            raise TypeError('frame number is required to be an int')
        image = self.read_frames(frame_number)[0, :, :]

        def line_select_callback(eclick, erelease):
            'eclick and erelease are the press and release events'
            x1, y1 = eclick.xdata, eclick.ydata
            x2, y2 = erelease.xdata, erelease.ydata


        def toggle_selector(event):
            if event.key in ['Q', 'q'] and toggle_selector.ES.active:
                toggle_selector.ES.set_active(False)
                plt.close()

        fig, ax = plt.subplots()
        ax.imshow(image)
        fig.tight_layout()

        toggle_selector.ES = EllipseSelector(ax, line_select_callback,
                                             drawtype='box', useblit=True,
                                             button=[1, 3],  # don't use middle button
                                             minspanx=5, minspany=5,
                                             spancoords='pixels',
                                             interactive=True,
                                             lineprops=dict(color='black', linestyle='-',
                                                            linewidth=2, alpha=0.5))
        plt.connect('key_press_event', toggle_selector)
        plt.show()
        def ellipse_dimensions(extents):
            center = (abs(extents[0] - extents[1]) / 2 + min(extents[0:2]),
                  abs(extents[2] - extents[3]) / 2 + min(extents[2:]))
            radius = (abs(extents[0] - extents[1]), abs(extents[2] - extents[3]))
            return center, radius[0], radius[1]

        self.roi_center, self.roi_width, self.roi_height= ellipse_dimensions(toggle_selector.ES.extents)
        roi_patch = mp.Ellipse(self.roi_center, self.roi_width, self.roi_height, fill=False, hatch='\\')
        return roi_patch

    def crop_from_roi(self):
        try:
            self.roi_center
            self.roi_width
            self.roi_height
        except AttributeError:
            roi_patch = self.define_roi()

        mask_array = np.ones((1, self.data_attributes['height'],
                             self.data_attributes['width']), dtype=bool)
        print(self.roi_center, self.roi_height, self.roi_width)
        for x, y in it.product(range(self.data_attributes['height']),
                               range(self.data_attributes['width'])):
            if self.in_ellipse(x, y, self.roi_center, self.roi_height, self.roi_width):
                print(x,y)
                mask_array[0, x, y] = False

        masked_image = np.ma.MaskedArray(self.read_frames(0), mask_array)
        fig, ax = plt.subplots(sharex='all', sharey='all')
        ax.add_artist(roi_patch)
        ax.imshow(masked_image[0, :, :])

        plt.show()
        return masked_image

    @staticmethod
    def in_ellipse(x, y, center, width_x, height_y):
        return (x-center[0])**2 * (height_y)**2 +\
               (y-center[1])**2 * (width_x)**2 <= 0.25 * height_y**2 * width_x**2

    def background_subratction(self):
        return None
