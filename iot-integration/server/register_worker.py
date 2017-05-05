import pika, sys, json

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config
from db.mongo import Mongo

class RegisterWorker(object):

    def __init__(self, rabbitmq_ip, queue_name, db_ip, db_port, db_name, collection_name):
        self.collection_name = collection_name
        self.db = Mongo(db_ip, db_port, db_name)
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=queue_name)
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):    
        print "Receive %s"%body
        item = json.loads(body)
        result = self.register(item)
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=result)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def register(self, item):
        items = self.db.find(self.collection_name, {'id': item['id']})
        if items.count() == 0:
            print "Discover New Device %s" %item['id']
            self.db.insert(self.collection_name, item)
            items = self.db.find(self.collection_name, {'id': item['id']})
        if items.count() == 1:
            return items[0]['id']
        return "DB Error"

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.rabbitmq.get_ip()
    queue_name = config.register.get_queue_name()
    collection_name = config.register.get_collection_name()
    db_ip = config.db.get_ip()
    db_port = config.db.get_port()
    db_name = config.db.get_name()
    worker = RegisterWorker(rabbitmq_ip, queue_name, db_ip, db_port, db_name, collection_name)
    while True:
        try:
            worker.start()
        except KeyboardInterrupt:
            print "[INFO] Detect Ctrl+C ... Worker Stop"
            sys.exit()
        except Exception as exception:
            print exception
            #if type(exception).__name__ == "ConnectionClosed":
            #    # print "Reconnecting ... "
            #    pass
            #pass
