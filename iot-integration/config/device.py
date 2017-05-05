from abstract import Abstract

class Device(Abstract):

    def get_interval(self):
        return int(self.cfg.get('device', 'interval'))
