import threading
import socket
from image_viewer import ImageViewer
from PIL import Image, ImageTk
from scipy.misc import imshow
from sys import argv
import pyautogui 
import pickle 
INTERVAL = 50


class Client(object):
    def __init__(self):
        self.running = True
        self.server_host = argv[1]
        self.my_socket = None
        self.image_viewer = ImageViewer(interval=INTERVAL)
        self.shape = None

    # connect client with the server to start chatting
    def run(self):
        # Create Client socket
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the Socket to server host and same port number
        self.my_socket.connect((self.server_host, 5555))
        # receive image shape
        self.shape = pickle.loads(self.my_socket.recv())
        
        print(self.shape)
        # Receiving Messages from Server on separate thread
        threading.Thread(target=self.receive).start()
        # run stream_viewer3
        # stream viewer should run in the main thread.
        self.image_viewer.next()
        self.image_viewer.slide_show()

    # Receive stream from Server
    def receive(self):
        size = (3 * self.shape[0] * self.shape[1] )+ self.shape[2]
        self.shape = self.shape[:1]
        wait = False
        temp = None
        while self.running:
            try:
                # receive file
                file = self.my_socket.recv(size)
                if len(file) < size:
                    if temp is None:
                        temp = file
                    else:
                        temp += file
                    # print(len(temp))
                    if len(temp) == size:
                        data = pickle.loads(temp)
                        self.image_viewer.add_frame(ImageTk.PhotoImage(Image.frombytes('RGB', self.shape, data[0])))
                        pyautogui.moveTo(data[1])
                        temp = None
                else:
                    data = pickle.loads(file)
                    self.image_viewer.add_frame(ImageTk.PhotoImage(Image.frombytes('RGB', self.shape, data[0])))
                    pyautogui.moveTo(data[1])
                    # print('received')
                    # imshow(Image.frombytes('RGB', (800, 800), file))
            except socket.error as msg:
                print('EXCEPTION ' + msg)

    # Ending stream
    def kill(self):
        self.running = False
        # Close chat socket
        self.my_socket.close()


if __name__ == '__main__':
    my_client = Client()
    my_client.run()