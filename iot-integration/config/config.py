import ConfigParser

from rabbitmq import Rabbitmq
from device import Device
from register import Register
from status import Status
from controller import Controller
from db import Db

class Config(object):
    def __init__(self):
        cfg = ConfigParser.ConfigParser()    
        cfg.read("/opt/iot-integration/config.ini")
        self.rabbitmq = Rabbitmq(cfg)
        self.device = Device(cfg)
        self.register = Register(cfg)
        self.status = Status(cfg)
        self.controller = Controller(cfg)
        self.db = Db(cfg)
