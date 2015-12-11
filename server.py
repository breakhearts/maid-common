"""
simple sever framework
"""
import zmq
import cPickle

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

ZMQ_SERVER_DEFAULT_SETTINGS = {
    "ip" : "127.0.0.1",
    "client_port":9300,
    "worker_port":9301
}

class ZmqTaskServer(SimpleServer):
    """
    distributed task publish server base on zmq
    """
    def __init__(self, **settings):
        self.settings = ZMQ_SERVER_DEFAULT_SETTINGS
        self.settings.update(settings)
        self.context = zmq.Context()
        self.client_socket = self.context.socket(zmq.ROUTER)
        self.worker_socket = self.context.socket(zmq.ROUTER)
        self.workers = []
        self.poller = zmq.Poller()

    def setup(self):
        self.client_socket.bind("tcp://*:%d" % self.settings["client_port"])
        self.worker_socket.bind("tcp://*:%d" % self.settings["worker_port"])
        self.poller.register(self.worker_socket)

    def run(self):
        r = self.poller.poll(0.1)
        for socket, evt in r:
            if socket == self.worker_socket:
                request = self.worker_socket.recv_multipart()
                worker, empty, client = request[:3]
                if not self.workers:
                   self.poller.register(self.client_socket)
                self.workers.append(worker)
                if client !=b"READY" and len(request) > 3:
                    empty, reply = request[3: ]
                    self.client_socket.send_multipart([client, b"", reply])

            elif socket == self.client_socket:
                client, empty, task = self.client_socket.recv_multipart()
                worker = self.workers.pop(0)
                self.worker_socket.send_multipart([worker, b"", client, b"", task])
                if not self.workers:
                    self.poller.unregister(self.client_socket)

class ZmqTaskServerClient:
    """
    client of zmq task server
    """
    def __init__(self, **settings):
        self.settings = ZMQ_SERVER_DEFAULT_SETTINGS
        self.settings.update(settings)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

    def connect(self):
        self.socket.connect("tcp://%s:%d" % (self.settings["ip"], self.settings["client_port"]))

    def send_task(self, task):
        self.socket.send(cPickle.dumps(task))
        t = self.socket.recv()
        t = cPickle.loads(t)

class ZmqTaskWorker(SimpleServer):
    """
    distributed task worker server base on zmq
    """
    def __init__(self, **settings):
        self.settings = ZMQ_SERVER_DEFAULT_SETTINGS
        self.settings.update(settings)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%d" % (self.settings["ip"], self.settings["worker_port"]))
        self.socket.send(b"READY")

    def do_task(self, task):
        print task

    def run(self):
        address, empty, task = self.socket.recv_multipart()
        t = self.do_task(task)
        self.socket.send_multipart([address, b"", cPickle.dumps(t)])