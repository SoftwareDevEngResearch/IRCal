import pytest
from ..tools import black_body_interface as bbi
import subprocess
import serial
import string
import time


def test_checksum():
    test_object = bbi.BlackBodyCommands()
    sample_checksum_string = b'W090'
    expected_output = b'H8'
    output = test_object.calculate_checksum(sample_checksum_string)
    assert output == expected_output


def test_create_byte_array():
    test_object = bbi.BlackBodyCommands()
    test_byte_array = test_object.create_command_byte_array(b'W0910.123G7')
    expected_byte_array = b'$0101W0910.123G7\r'
    assert test_byte_array == expected_byte_array