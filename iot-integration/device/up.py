import json, threading, time, os, sys

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config
from device.register import Register
from device.device import Device
from device.reporter import Reporter
from device.controller import Controller

class Job(object):
    def __init__(self, device, rabbitmq_ip, register_queue, status_queue, control_queue):
        self.device = device
        self.rabbitmq_ip = rabbitmq_ip
        self.register_queue_name = register_queue
        self.status_queue_name = status_queue
        self.control_queue_name = control_queue

    def register(self):
        id = self.device.cpu.get_sn()
        msg_obj = {
            'cmd': 'register',
            'state': 'new',
            'id': id,
            'name': 'Room Device', 
            'ip': self.device.network.get_ip_address('eth0'),
            'sensor_type': 'Thermal', 
            'additional': 'LED',
            'cpu_model': self.device.cpu.get_model(),
            'memory_size': self.device.memory.get_size(),
            'disk_size': self.device.disk.get_size(),
            'timestamp': int(time.time())
        }  
        msg = json.dumps(msg_obj)  

        with Register(self.rabbitmq_ip, self.register_queue_name) as task:
            print "[Info - Register] Register Start"
            response = task.call(msg)
        return response == id

    def report(self, interval):
        print "[Info - Reporter] Thread Start"
        while True:
            msg_obj = {
                'id': self.device.cpu.get_sn(),
                'ip': self.device.network.get_ip_address('eth0'),
                'cpu_temp': self.device.cpu.get_temps(),
                'cpu_usage': self.device.cpu.get_usage(),
                'memory_usage': self.device.memory.get_usage(),
                'disk_usage': self.device.disk.get_usage(),
                'traffic': self.device.network.get_traffic(),
                'temp': self.device.addon.get_thermal(),
                'led': self.device.addon.led.get(),
                'timestamp': int(time.time())
            }
            msg = json.dumps(msg_obj)  
            with Reporter(self.rabbitmq_ip, self.status_queue_name) as reporter:
                reporter.call(msg)

            print "[Info - Reporter] reporting %s"%msg
            time.sleep(interval)
        
    def controller(self):
        print "[Info - Controller] Thread Start"
        while True:
            try:
                worker = Controller(self.rabbitmq_ip, self.control_queue_name, self.device)
                worker.start()       
            except Exception as exception:
                pass

if __name__ == "__main__":
    print "[Info - Main] Service Start ... "

    config = Config()
    rabbitmq_ip = config.rabbitmq.get_ip()
    reqister_queue = config.register.get_queue_name()
    status_queue = config.status.get_queue_name()
    control_queue = config.controller.get_queue_name()    
    interval = config.device.get_interval()
    device = Device()
    job = Job(device, rabbitmq_ip, reqister_queue, status_queue, control_queue)
    while True:
        if job.register() == True:
            print "[Info - Register] Register Success"
            print "[Info - Main] Sleep %s Seconds" %interval
            time.sleep(interval)
            threading.Thread(target = job.report, args = {interval}, name = "reporter-thread").start()
            threading.Thread(target = job.controller, args = {}, name = "controller-thread").start()
            exit()
        else:
            time.sleep(interval*10)

