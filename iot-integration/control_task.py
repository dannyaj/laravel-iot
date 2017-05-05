import pika
import uuid
import json
import sys
from config.config import Config

class Task(object):
    def __init__(self, rabbitmq_ip):
        self.rabbitmq_ip = rabbitmq_ip
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_ip))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)
        # return self

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, power):
        msg = {'power': power}
        msg = json.dumps(msg)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='control_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=msg)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.rabbitmq.get_ip()
    task = Task(rabbitmq_ip)
    response = task.call(sys.argv[1])
    print(" [.] Got %r" % response)
