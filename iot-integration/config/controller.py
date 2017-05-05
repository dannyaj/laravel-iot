from abstract import Abstract

class Controller(Abstract):

    def get_queue_name(self):
        return self.cfg.get('control', 'queue_name')
