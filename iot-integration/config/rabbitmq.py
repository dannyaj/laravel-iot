from abstract import Abstract

class Rabbitmq(Abstract):

    def get_ip(self):
        return self.cfg.get('rabbitmq-cluster', 'ip')