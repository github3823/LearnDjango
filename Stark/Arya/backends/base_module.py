

class BaseSaltModule(object):
    def __init__(self,sys_args):
        self.sys_agrs = sys_args
        self.fetch_hosts()


    def fetch_hosts(self):
        print('fetching hosts')

