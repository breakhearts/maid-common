from stockmaid.spidermaid.spidermaid.common.server import *

if __name__ == "__main__":
    client = ZmqTaskServerClient()
    client.connect()
    while True:
        client.send_task(1234)