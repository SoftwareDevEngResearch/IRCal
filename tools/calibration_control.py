from black_body_interface import BlackBodyCommands as BSC
from image_analysis import ImageTools as imgt
import pyyaml
import time
import scipy.optimize.curve_fit as fit_tool

'''
Control code to execute a black body calibration of an infrared thermography device
This is currently just an outline of the functions and functionality.
In the future it will probably be formatted into a class in the future
@author: Derek Bean
'''

def read_imput(file_name):
    return camera_settings, temperature_profile

def verify_connections(camera_object, blackbody_object):
      """
         Runs the commands that verify connection to the devices.
         The methods called will raise errors if unsuccessful
      """
        blackbody_object.configure_port()
        camera_object.verify_connection()
        return None

def configure_camera(camera_object, camera_settings):
    camera_object.setup(camera_settings)
    return None

def calibrate(camera_object, blackbody_object, temperature_profile, std_threshold):
    '''
    Perform the camera calibration procedure based on the inputs
    :param camera_object:
    :param blackbody_object:
    :param temperature_profile:
    :param std_threshold:
    :return:
    '''
    for temperature in temperature_profile:
        blackbody_object.set_temperature(temperature)
        temp_reading = blackbody_object.read_temperature()
        # check the temperature every 5 min until the thermocouple in the blackbody reads the setpoint
        # this only works for increasing temperatures and will be modified for both directions in the future
        while temp_reading < temperature:
            time.sleep(300)
            temp_reading = blackbody_object.read_temperature()
            print('The current blackbody temperature is {0} deg C below the setpoint'.format(temp_reading-temperature))
        # now that the blackbody reads the setpoint switch to image uniformity
        image_std = imgt.std(camera_object.get_frame())
        while image_std > std_threshold:
            time.sleep(300)
            image_std = imgt.std(camera_object.get_frame())
        # now that the image is acceptably uniform save the image
        # this will be formatted into a hdf5 dataset with the temperatures and camera information
        camera_object.save_frame(image_folder)

def correlate_counts(image_folder, temperatures):
    '''
    read in the calibration image dataset and get the mean counts and correlate to temperature
    :param image_folder:
    :param temperatures:
    :return:
    '''

    calibration_data = imgt.read_frames(image_folder)
    # this won't work in the current package. need to add this in the future
    mean_data = [calibration_data.frame_mean(idx) for idx, val in enumerate(calibration_data)]
    correlation = fit_tool(temperatures, mean_data)
    return correlation

def cool_down(blackbody_object):
    # cool down the blackbody to room temperature
    blackbody_object.cool_down()







