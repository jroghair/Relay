# plug in for the tim 551 lidar
# puts data into the queue in (angle, distance) pairs

import queue as q
import socket
import matplotlib.pyplot as plt
import pylab
import time

one_scan_request = bytes(
    [0x02, 0x73, 0x52, 0x4E, 0x20, 0x4C, 0x4D, 0x44, 0x73, 0x63, 0x61, 0x6E, 0x64, 0x61, 0x74, 0x61, 0x03])


class tim_551_component:

    def __init__(self, inputQueue, outputQueue, visualize):
        self.outputQueue = outputQueue
        self.inputQueue = inputQueue
        self.ip = '169.254.185.233'
        self.port = 2112
        self.buffer = 1500
        self.num_points = 271
        self.return_data = []
        self.vis = visualize
        print("Starting tim_551_component")
        self.run()

    def run(self):
        # if self.vis:
        #     ax2 = plt.subplot(212, projection="polar")
        count = 0
        while 1:
            count += 1
            self.current_ang = -45
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s.send(one_scan_request)
            data = s.recv(self.buffer)
            s.close()

            # process data

            data = data.split()

            self.return_data = []
            for x in range(0, self.num_points):
                self.current_ang += 1
                if(self.current_ang == -18 or self.current_ang == -19):
                    continue
                if((int(data[25 + x], 16) / 1000) < .05):
                    continue
                self.return_data.append((self.current_ang-1, (int(data[25 + x], 16) / 1000)))

            theta = [x * 3.14159 / 180 for x in [i[0] for i in self.return_data]]
            radii = [i[1] for i in self.return_data]
            # put data into the queue
            if(self.outputQueue.qsize() == 0):
                self.outputQueue.put(self.return_data)
            else:
                self.outputQueue.get()
                self.outputQueue.put(self.return_data)

            if self.vis:
                ax2 = plt.subplot(212, projection="polar")
                ax2.cla()



                ax2.scatter(theta, radii, c=radii, s=100, cmap='hsv', alpha=0.75)
                ax2.set_ylim((0, 10))
                plt.pause(0.05)
                #
                # self.ax1.scatter(theta, radii, c=radii, s=100, cmap='hsv', alpha=0.75)
                # plt.pause(0.05)

            self.return_data = []

# def main():
#     print("starting lidar plug in")
#     data_q = q.Queue()
#     lidar = lidar_plug_in(data_q, '169.254.185.233', 2112, True)
#     lidar.run()


# if __name__ == "__main__":
#     main()
