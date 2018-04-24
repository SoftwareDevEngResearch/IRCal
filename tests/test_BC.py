#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:34:50 2018

@author: aero-10
"""

from IRCal.tools.blackbody_connect import BlackBody_Control as BC
import pytest
import os

def test_write_file():
    ''' Test to evaluate the write file function. 
        Current functionality: test to make sure the files are the same
        Future functionality: look for unicode errors and possibly some
                              formatting
    '''
    filename = '/home/aero-10/Documents/SoftwareClass/IRCal/IRCal/tests/test_files/hello_world.c'
    
    def file_lines(filename):
        text = []
        with open(filename) as f:
            for line in f:
                text.append(line)
        return text
    
    write_test = BC()
    fpath = write_test.write_file(file_lines(filename))
    assert all(i == j for i, j in zip(file_lines(filename), file_lines(fpath)))
    
    
def test_compile_file():
    ''' Test the fuctionality of the compile file function to see if it
        compiles the ouput file without errors. The success of the compile
        file function also relies on the correct inputs to the write file
        fuction which will be implemented in the future'''
    test_path = os.path.expanduser('~/Documents/SoftwareClass/IRCal/IRCal/tests/test_files')
#    test_command = "gcc -o hello hello_world.c"
    compile_test = BC()
#    os.chdir(test_path)
    commands = ["gcc",  "-o", "hello", "hello_world.c"]
    compile_test.compile_file(commands)
    assert os.path.isfile(os.path.join(test_path, 'hello')) == True
        
def test_execute_file():
    program_name = os.path.expanduser('~/Documents/SoftwareClass/IRCal/IRCal/tests/test_files/hello')
    execute_test = BC()
    output = execute_test.run_program(program_name)
    assert output.strip() == b'hello, world'
    
