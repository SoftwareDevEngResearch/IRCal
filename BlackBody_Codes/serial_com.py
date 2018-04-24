# 4/24/2018

import subprocess
import serial



class BlackBody_Serial():
	def __init__():
		self.ports = subprocess.check_output(['python', '-m',
                                                     'serial.tools.list_ports']).decode('utf-8').\
                                                     strip('\n').replace('\n', '').split()
