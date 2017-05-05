from cpu import CPU
from memory import Memory
from disk import Disk
from network import Network
from addon import Addon

class Device(object):

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()
        self.network = Network()
        self.addon = Addon()

