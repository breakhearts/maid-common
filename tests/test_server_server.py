from stockmaid.spidermaid.spidermaid.common.server import *

if __name__ == "__main__":
    server = ZmqTaskServer()
    server.start()