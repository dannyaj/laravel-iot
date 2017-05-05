import os, psutil

class Disk(object):

    def __init__(self):
        pass

    def get_size(self):
        format_string = [ 'B', 'KB', 'MB', 'GB', 'TB' ]
        index = 0
        try:
            st = os.statvfs('/')
            size = float(st.f_blocks * st.f_frsize)
            while size > float(1000):
                size = round(size / float(1000))
                index = index + 1
            size = "%s %s"%(int(size), format_string[index])
            return size
        except:
            return "Unknown"

    def get_usage(self):
        return psutil.disk_usage('/').percent