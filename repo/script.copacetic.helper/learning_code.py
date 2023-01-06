#v2:
class Main:
    def __init__(self, *args):
        self.params = {}
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                self.params[key] = value.strip('\'').strip('"')
            else:
                self.params[arg] = True
        function = eval(self.params['action'])
        function(**self.params)


#v3:
class Main:
    def __init__(self, *args):
        try:
            self.params = dict(arg.split('=', 1) for arg in args)
        except:
            self.params = {}
        function = eval(self.params['action'])
        function(**self.params)