from abstract import Abstract

class Register(Abstract):

    def get_queue_name(self):
        return self.cfg.get('register', 'queue_name')

    def get_collection_name(self):
        return self.cfg.get('register', 'collection')
