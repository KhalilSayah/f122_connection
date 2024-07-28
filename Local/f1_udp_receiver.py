import socket
from queue import Queue
from typing import Optional
import threading
import signal
import time
import pickle


class UDPParser:
    def __init__(self):
        self.udp_port = 20777
        self.udp_host = "0.0.0.0"
        self.udp_socket: Optional[socket.socket] = None
        self.stop_event = threading.Event()
        self.packets = Queue[bytes]()

    def _receiver(self):
        self.udp_socket.bind((self.udp_host, self.udp_port))
        print(f"Listening for UDP packets on port {self.udp_port}...")
        while not self.stop_event.is_set():
            try:
                data, addr = self.udp_socket.recvfrom(65507)  # Buffer size is 65507 bytes
                self.packets.put(data)
            except socket.error as e:
                print(f"Socket error: {e}")
        print("Receiver thread is stopping...")

    def _saver(self):
        while not self.stop_event.wait(60):  # Wait for 1 minute
            self.save_queue()

    def save_queue(self):
        packets_list = list(self.packets.queue)  # Convert Queue to list
        with open('packets.pkl', 'wb') as file:
            pickle.dump(packets_list, file)
        print("Queue saved to packets.pkl")

    def start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        receiver_thread = threading.Thread(target=self._receiver)
        receiver_thread.daemon = True
        receiver_thread.start()

        saver_thread = threading.Thread(target=self._saver)
        saver_thread.daemon = True
        saver_thread.start()

        try:
            receiver_thread.join()
        except KeyboardInterrupt:
            print("Stopping...")
            self.stop_event.set()
            receiver_thread.join()
            saver_thread.join()

if __name__ == "__main__":
    parser = UDPParser()
    parser.start()
