"""
Interface with an Electro Optical Industries Blackbody Radiation Source
Temperature Controller Model 2500E/R

author: Derek Bean
"""


class BlackBody_Control():
    """Control and interface with the blackbody temperature controller over
       a RS232 connection using c programs written and compiled with python
    """
    def __init__(self):
        return

    def write_file(self, input_text):
    """Generate a c file that can be used to communicate with the blackbody
    in the desired way. The initial text file is just a hello world C script
    that is imported with future options to recive text input from the command
    line among other options
    """
        return
    def compile_file(self):
    """ Compile the C file to create a an executatble c file. Eventually this
    will work for both Windows and Linux but it will initially be linux only
    """
        return
    def run_program(self):
    """Execute the previously compiled program for the communication protocol
    """
        return
