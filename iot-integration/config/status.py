from abstract import Abstract

class Status(Abstract):

    def get_queue_name(self):
        return self.cfg.get('status', 'queue_name')
        
    def get_collection_name(self):
        return self.cfg.get('status', 'collection')