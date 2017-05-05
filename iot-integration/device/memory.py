import psutil

class Memory(object):

    def __init__(self):
        pass

    def get_size(self):
        format_string = [ 'KB', 'MB', 'GB', 'TB' ]
        index = 0
        try:
            with open('/proc/meminfo','r') as f:
                for line in f:
                    if line[0:8]=='MemTotal':
                        line = ' '.join(line.split())
                        size = float(line[10:-3])
                        while size > float(1024):
                            size = round(size / float(1024))
                            index = index + 1
                        size = "%s %s"%(int(size), format_string[index])
        except:
            return "Unknown"
        return size

    def get_usage(self):
        return psutil.virtual_memory().percent