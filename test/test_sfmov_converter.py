from ..tools import  sfmov_converter as sc
import os
import numpy as np
import pytest

os.chdir('test/test_files/')

def test_scrape_inc():
    filepath = os.path.abspath('.')
    test_object = sc.SfmovTools(filepath, filepath, 'ir_test_file')
    test_frame_rate, test_inc_time, test_camera_name = test_object.scrape_inc()
    assert np.isclose(test_frame_rate, 125.00)
    assert np.isclose(test_inc_time, 1.5)
    assert test_camera_name == b'SC6700'

def test_imread():
    filepath = os.path.abspath('.')
    test_object = sc.SfmovTools(filepath, filepath, 'ir_test_file')
    data, dimensions, number_of_frames, dropped_frames = test_object.scrape_sfmov()
    assert (dimensions == {'height': 512, 'width': 368})
    assert (number_of_frames == 10)
    assert (dropped_frames == 0)


def test_convert():
    filepath = os.path.abspath('.')
    filename = ('ir_test_file')
    try:
        os.remove(os.path.join(filepath, filename+'.hdf5'))
    except FileNotFoundError:
        pass
    test_object = sc.SfmovTools(filepath, filepath, filename)
    test_object.convert()
    assert os.path.isfile(os.path.join(filepath, 'ir_test_file.hdf5'))
    with pytest.raises(OSError, match='The file already exists please choose a different one or delete the file'):
        test_object.convert()
    # os.remove(os.path.join(filepath, filename + '.hdf5'))
