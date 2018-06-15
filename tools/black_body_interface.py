# 4/24/2018

import subprocess
import serial
import string
import time


class BlackBodySerialCommunication:
    """
    Basic functions for configuring reading and writing related to the blackbody

    This class holds the basic functions that can be used to communicate with the black body.
    This includes configuring the port, opening and closing the port as well as reading and writing
    to the device. This class is meant to be a parent class to other functions that need to
    read/write/configure to do their task
    """
    # TODO: Add a function that checks for error in the message ans notifies the user

    def __init__(self, verbose=False):
        """Determine the currently connected serial ports that can be used
        for serial communication"""
        self.ports = subprocess.check_output(['python', '-m',
                                             'serial.tools.list_ports']).decode('utf-8').\
                                              strip('\n').replace('\n', '').split()
        self.start_char = b"$"
        self.end_char = b"\r"
        self.id_char = b"0101"
        self.read_char = b'R'
        self.write_char = b"W"
        self.verbose = verbose

    def configure_port(self, port_number=0, timeout=5):
        """Setup the port based on the specs for the blackbody device
        as defined by the user manual. See the docs for the user manual"""
        # TODO: May be possible to automatically determine and set the port number
        self.port_name = self.ports[port_number]
        self.configured_port = serial.Serial(self.ports[port_number],
                                             bytesize=serial.EIGHTBITS,
                                             parity=serial.PARITY_NONE,
                                             stopbits=1,
                                             baudrate=9600,
                                             timeout=timeout)

    def open_port(self):
        """Check to see fo the port is open and open it if not open"""
        if self.port_status:
            if self.verbose:
                print('{0} is Open'.format(self.port_name))
        else:
            self.configured_port.open()
            self.open_port()

    def close_port(self):
        """Check to see if the port is closed and close it if open"""
        if not self.port_status:
            if self.verbose:
                print('{0} is Closed'.format(self.port_name))
        else:
            self.configured_port.close()
            self.close_port()

    @property
    def port_status(self):
        """Check the state of the port (open or closed)
        Returns true for open and false for closed"""
        try:
            if self.configured_port.is_open():
                return True
            elif not self.configured_port.is_open():
                return False
        except:
            self.configure_port()
            self.port_status

    def write_message(self, write_data):
        """Write a message over the serial connection. Requires a byte string"""
        if type(write_data) == bytes:
            self.open_port()
            self.configured_port.write(write_data)
        else:
            raise TypeError('The write_message function requires an input of type bytes')

    def read_message(self):
        """Read the serial output from the connection. Returns a byte string"""
        self.open_port()
        return self.configured_port.readline()


class BlackBodyCommands(BlackBodySerialCommunication):

    def get_param_value(self, type):
        if type == b'R':
            self.param = b'05'
            return self.param
        elif type == b'W':
            self.param = b'09'
            return self.param
        else:
            raise ValueError('The type submitted was not a byte sting of R or W')

    def calculate_checksum(self, input_string):
        """calculate the value of the checksum that must be added to the end of all commands sent to the device"""
        # letter values are the number representation of the values used to build the cheksum command.
        # See the blackbody manual (pg.8) for more information
        letter_values = {100 + (val * 10): letter for val, letter in enumerate(list(string.ascii_uppercase))}
        calculate_string = b''.join([self.id_char, input_string])
        checksum_number = sum(calculate_string) % 256
        letter_number = checksum_number - (checksum_number % 10)
        remainder = checksum_number - letter_number
        def to_bytes(value):
            return bytes(str(value), encoding='utf8')
        return b''.join([to_bytes(letter_values[letter_number]), to_bytes(remainder)])

    def create_command_byte_array(self, stripped_message):
        return b''.join([self.start_char, self.id_char, stripped_message, self.end_char])

    def set_temperature(self, temperature):
        """Change the setpoint of the blackbody. temperature must be a byte array 6 characters in length
        including the . if one is included. the temperature units are deg C"""
        # TODO error handling for the temperature string
        type = b'W'
        base_message = b''.join([type, self.get_param_value(type), temperature])
        stripped_message = b''.join([base_message, self.calculate_checksum(base_message)])
        self.write_message(self.create_command_byte_array(stripped_message))
        return self.read_message()

    def read_temperature(self):
        """Read the current temperature of the blackbody"""
        type = b'R'
        self.write_message(b'$0101R05C1\r')  # Predefined command as set by the manual
        time.sleep(0.1)
        response = self.read_message()
        decoded_message = self.decompose_message(response)
        self.close_port()
        print(response)
        print(self.check)
        return str(decoded_message['data'])

    def decompose_message(self, message):
        """Convert the message read form the device to a dictionary of its components"""
        return {'start_char': message[0], 'id': message[1:5], 'type': message[5:6],
                'param': message[6:8], 'data': message[8:14], 'checksum': message[14:-1],
                'endchar': message[-1:]}

    def cool_down(self):
        '''
        Set the blackbody temp to 50 deg c to cool down to a safe temp before unplugging
        Ideally this would run and check temperatures at intervals and return when the
        blackbody is cool but it is not desirable to lock up a thread for the large amount
        of time this takes
        :return:
        '''
        self.set_temperature(b'000050')
        return None