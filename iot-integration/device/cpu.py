import os, psutil

class CPU(object):
    def __init__(self):
        pass

    def get_temps(self):
        # res = os.popen('vcgencmd measure_temp').readline()
        # return(res.replace("temp=","").replace("'C\n",""))
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            line = float(next(f))
                
        return round((line/1000), 1)

    def get_sn(self):
        cpu_serial = "0000000000000000"
        try:
            with open('/proc/cpuinfo','r') as f:
                for line in f:
                    if line[0:6]=='Serial':
                        cpu_serial = line[10:26]
        except:
            cpu_serial = "ERROR000000000"
        return cpu_serial

    def get_model(self):
        cpu_model = "ARMv7 Processor"
        try:
            with open('/proc/cpuinfo','r') as f:
                for line in f:
                    if line[0:10]=='model name':
                        cpu_model = line[13:-1]
                        # exit()
        except:
            cpu_model = "ERROR"
        return cpu_model

    def get_usage(self):
        return psutil.cpu_percent(interval=1)
