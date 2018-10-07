import queue as q
import serial
from time import sleep
import random


# from Arduino import Arduino

class Motor_Interface:

    def __init__(self, input_q, com_port, output_q, visualize):
        self.in_queue = input_q
        self.out_queue = output_q
        self.cp = com_port
        self.visualize = visualize
        self.run()

    def run(self):
        ser = serial.Serial(self.cp, 115200)
        sleep(3)

        while True:

            if self.in_queue.qsize() > 0:
                if self.visualize:
                    print("Motor interface queue size: " + str(self.in_queue.qsize()))
                command = self.in_queue.get()
                ser.write(bytes(command, 'utf-8'))
                # if (self.visualize):
                #     print("Command sent to arduino: " + str(command))
            else:
                ser.write(b's')
                # if (self.visualize):
                #     print("Command sent to arduino: " + str('s'))

            sleep(.02)

# def main():
# 	input_queue = q.Queue()
# 	output_queue = q.Queue()
# 	input_queue.put('f')
# 	input_queue.put('l')
# 	input_queue.put('r')
# 	input_queue.put('f')
# 	input_queue.put('l')
# 	input_queue.put('r')
# 	input_queue.put('f')
# 	input_queue.put('l')
# 	input_queue.put('f')
# 	motor_interface = dif_drive_motor_plugin(input_queue, output_queue, 'COM6')
# 	motor_interface.run()

# if __name__ == "__main__":
# 	main()
