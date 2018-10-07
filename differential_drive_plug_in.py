import serial

class dif_drive_motor_plugin:

	def __init__(self, input_q, output_q):
		self.input_q = input_q;

	def run(self):
		while 1:
