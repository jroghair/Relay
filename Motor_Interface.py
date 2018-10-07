import queue

class Motor_Interface_backup:
    def __init__(self, inputQueue1, input2, outputQueue, vis):
        self.inputQueue = inputQueue1
        self.COMPortString = input2
        self.outputQueue = outputQueue
        self.visualize = vis
        self.run()

    def run(self):
        while True:
            if(self.inputQueue.qsize()>0):
                driveChar = self.inputQueue.get()
