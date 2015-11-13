"""
simple sever framework
"""

class SimpleServer:
    def __init__(self):
        pass

    def run(self):
        pass

    def setup(self):
        pass

    def tear_down(self):
        pass

    def before_run(self):
        pass

    def after_run(self):
        pass

    def start(self):
        self.setup()
        while True:
            try:
                self.before_run()
                self.run()
                self.after_run()
            except (KeyboardInterrupt, SystemExit):
                self.tear_down()
                break