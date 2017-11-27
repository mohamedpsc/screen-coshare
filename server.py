import socket
import threading
import time
import pyscreenshot as ImageGrab

IMAGE_SIZE = 800, 800
PORT_NUMBER = 5555


class Server():
    def __init__(self):
        self.running = True
        self.socket = None
        self.client_socket = None
        self.client_address = None

    @staticmethod
    def get_screen():
        return ImageGrab.grab().resize(IMAGE_SIZE).tobytes()

    def run(self):
        # Create server socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the Socket to a public host
        self.socket.bind(('', PORT_NUMBER))
        # Max Number of connections allowed is 1
        self.socket.listen(1)
        # Accepting connection from client
        print('Listening on port ' + str(PORT_NUMBER))
        self.client_socket, self.client_address = self.socket.accept()
        print('connected to ' + str(self.client_address))
        # Receiving clients commands on separate thread
        threading.Thread(target=self.receive).start()
        # sending screen shot dimension
        self.client_socket.send(str(IMAGE_SIZE).encode())
        # Sending screenshots
        while self.running:
            self.send_image()
            time.sleep(0.3)

    def send_image(self):
        screen_shot = self.get_screen()
        self.client_socket.sendall(screen_shot)

    def receive(self):
        """
        Receive commands from client
        """
        while self.running:
            pass

    def kill(self):
        """
        Close Sockets
        """
        self.running = False
        self.client_socket.close()


if __name__ == '__main__':
    server = Server()
    server.run()
