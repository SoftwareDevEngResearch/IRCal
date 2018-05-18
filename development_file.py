"""
This file is used to test the functionality of the modules and functions under development and to help
with creating tests.
"""
from tools import black_body_interface as bbi
from tools import sfmov_converter as sc
from tools import image_analysis as ia
import os


if __name__ == '__main__':
    sfmov_path = os.path.join(os.path.abspath('.'), 'test/test_files/')
    file_name = "B-lab test-000002"
    se = sc.SfmovTools(sfmov_path, sfmov_path, file_name)
    print(se.camera_name)
    se.convert()