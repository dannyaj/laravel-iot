import pika, sys

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config

class Reporter(object):
    def __init__(self, rabbitmq_ip, queue_name):
        self.rabbitmq_ip = rabbitmq_ip
        self.queue_name = queue_name

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        return self

    def call(self, msg):
        self.channel.basic_publish(
                   exchange='',
                   routing_key=self.queue_name,
                   body=msg,
                   properties=pika.BasicProperties(
                      delivery_mode = 2, # make message persistent
                   ))
        
    def __exit__(self, type, value, traceback):
        self.connection.close()

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.get_rabbitmq_ip()
    with StatusTask(rabbitmq_ip) as task:
        task.call("Hello World")