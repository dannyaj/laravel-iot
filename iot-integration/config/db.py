from abstract import Abstract

class Db(Abstract):

    def get_type(self):
        return self.cfg.get('type')

    def get_ip(self):
        return self.cfg.get('db', 'ip')

    def get_port(self):
        return self.cfg.get('db', 'port')

    def get_name(self):
        return self.cfg.get('db', 'name')