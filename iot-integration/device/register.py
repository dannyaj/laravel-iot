import pika, sys, uuid

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config

class Register(object):
    def __init__(self, rabbitmq_ip, queue_name):
        self.rabbitmq_ip = rabbitmq_ip
        self.queue_name = queue_name

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_ip))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        return self

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def __exit__(self,  type, value, traceback):
        self.connection.close()

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.get_rabbitmq_ip()
    queue_name = config.get_register_queue_name()
    with Register(rabbitmq_ip, queue_name) as task:
        response = task.call("%s %s"%(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time())), uuid.uuid4()))
        
    print(" [.] Got %r" % response)
