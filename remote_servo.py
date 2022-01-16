import websocket
import threading
import logging


class RemoteServoConnection:
    def __init__(self, mulitplier = 1, offset = 0):
        self.mulitplier = mulitplier
        self.offset = offset

        self.ws = websocket.WebSocketApp("ws://jkostecki.ddns.net:1111")
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def set(self, x, z):
        if not self.ws.sock.connected:
            logging.error("WebSocket isn't connected.")
            return

        self.ws.send(('%.2f' % x) + "," + ('%.2f' % z))

