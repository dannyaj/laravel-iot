import pika, time, sys, json

sys.path.insert(0, '/opt/iot-integration')

from config.config import Config

class Controller(object):
    def __init__(self, rabbitmq_ip, queue_name, device):
        self.device = device
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=queue_name)

    def on_request(self, ch, method, props, body):    
        print "[Info - Controller] Got %s"%body
        try: 
            body = json.loads(body)
            resp = self.control_led(body)
        except:
            resp = "Error"

        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=resp)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def control_led(self, body):
        try:
            # if body["target"] == "white":
            #     led = self.device.addon.white_led
            # if body["target"] == "blue":
            #     led = self.device.addon.blue_led
            # if body["command"] == "on":
            #     led.on()
            # if body["command"] == "off":
            #     led.off()
            self.device.addon.led.set(body['power'])
            return "Success"
        except Exception as exception:
            print exception
            return "Failed"

    def start(self):
        self.channel.start_consuming()

    def __exit__(self):
        self.connection.close()

if __name__ == "__main__":
    config = Config()
    rabbitmq_ip = config.get_rabbitmq_ip()
    while True:
        try:
            worker = Controller(rabbitmq_ip)
            worker.start()
        except KeyboardInterrupt:
            print "[INFO] Detect Ctrl+C ... Worker Stop"
            sys.exit()
        except Exception as exception:
            if type(exception).__name__ == "ConnectionClosed":
                # print "Reconnecting ... "
                pass
            pass
