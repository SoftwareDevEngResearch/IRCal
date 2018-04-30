# 4/24/2018

import subprocess
from typing import Union

import serial
from serial import Serial

import string


class BlackBodySerial():

    def __init__(self):
        self.ports = subprocess.check_output(['python', '-m',
                                             'serial.tools.list_ports']).decode('utf-8').\
                                              strip('\n').replace('\n', '').split()

    def configure_port(self, port_number=0, timeout=5):
        self.port_name = self.ports[port_number]
        self.configured_port = serial.Serial(self.ports[port_number],
                                        bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=1,
                                        baudrate=9600,
                                        timeout=timeout)

    def open_port(self):
        if self.port_status:
            print('{0} is Open'.format(self.port_name))
        else:
            self.configured_port.open()
            self.open_port()

    def close_port(self):
        if not self.port_status:
            print('{0} is Closed'.format(self.port_name))
        else:
            self.configured_port.close()
            self.close_port()

    @property
    def port_status(self):
        if self.configured_port.is_open is True:
            return True
        elif self.configured_port.is_open is False:
            return False


    def write_message(self, write_data):
        self.open_port()
        self.configured_port.write(write_data)

    def read_message(self):
        self.open_port()
        return self.configured_port.readline()


    def read_temperature(self):
        self.write_message(b'$0101R05C1\r')
        response = self.read_message()
        self.close_port()
        return response

    def decode_message(self, message):
        letter_values = {letter: 100 + (val * 10) for val,
                                                      letter in enumerate(list(string.ascii_uppercase))}
        return letter_values

if __name__ == '__main__':
    a = BlackBodySerial()
    a.configure_port(0)
    b = a.read_temperature()
    print(b)
    print(a.decode_message('a'))

