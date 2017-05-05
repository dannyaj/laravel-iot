import pika, sys, json

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config
from db.mongo import Mongo

class StatusWorker(object):
    def __init__(self, rabbitmq_ip, queue_name, db_ip, db_port, db_name, collection_name):
        self.db = Mongo(db_ip, db_port, db_name)
        self.collection_name = collection_name

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=5)
        self.channel.basic_consume(self.callback, queue=queue_name)
        
        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)
        item = json.loads(body)
        self.db.insert(self.collection_name, item)

        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.rabbitmq.get_ip()
    queue_name = config.status.get_queue_name()
    collection_name = config.status.get_collection_name()
    db_ip = config.db.get_ip()
    db_port = config.db.get_port()
    db_name = config.db.get_name()
    while True:
        try:
            worker = StatusWorker(rabbitmq_ip, queue_name, db_ip, db_port, db_name, collection_name)
        except KeyboardInterrupt:
            print "[INFO] Detect Ctrl+C ... Worker Stop"
            sys.exit()
        except Exception as exception:
            print exception
            if type(exception).__name__ == "ConnectionClosed":
                # print "Reconnecting ... "
                pass
            pass
