import psutil
import socket, fcntl, struct


class Network(object):

    def __init__(self):
        traffic = psutil.net_io_counters()
        self.bytes_sent = traffic.bytes_sent
        self.bytes_recv = traffic.bytes_recv

    def get_traffic(self):
        traffic = psutil.net_io_counters()

        traffic_in = traffic.bytes_recv - self.bytes_recv
        traffic_out = traffic.bytes_sent - self.bytes_sent 

        self.bytes_sent = traffic.bytes_sent
        self.bytes_recv = traffic.bytes_recv

        return {'bytes_sent': traffic_out, 'bytes_recv': traffic_in}

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  
            struct.pack('256s', ifname[:15])
        )[20:24])
