#plug in for the tim 551 lidar

import queue

class lidar_plug_in:

	data_queue = queue.Queue()

	def __init__(self, queue):
		self.data_queue = queue
