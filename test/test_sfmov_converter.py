from ..tools import  sfmov_converter as sc
import os
import numpy as np


def test_scrape_inc():
    os.chdir('test/test_files/')
    filepath = os.path.abspath('.')
    test_object = sc.SfmovTools(filepath, filepath, 'ir_test_file')
    test_frame_rate, test_inc_time, test_camera_name = test_object.scrape_inc()
    assert np.isclose(test_frame_rate, 125.00)
    assert np.isclose(test_inc_time, 1.5)
    assert test_camera_name == 'SC6700'

def test_imread():
    os.chdir('C:/Users/derek/PycharmProjects/IRCal/test/test_files/')
    filepath = os.path.abspath('.')
    test_object = sc.SfmovTools(filepath, filepath, 'ir_test_file')
    data, dimensions, number_of_frames, dropped_frames = test_object.imread()
    assert (dimensions == {'height': 512, 'width': 368})
    assert (number_of_frames == 10)
    assert (dropped_frames == 0)