#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:34:50 2018

@author: aero-10
"""

from IRCal.tools.blackbody_connect import BlackBody_Control as BC
import pytest

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
    
    test1 = BC()
    fpath = test1.write_file(file_lines(filename))
    assert all(i == j for i, j in zip(file_lines(filename), file_lines(fpath)))
    
    
def test_compile_file():
    a = 0
    
def test_execute_file():
    a = 0
    
