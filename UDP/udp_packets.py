import socket
from queue import Queue
from typing import Optional
import threading
import signal
from Filters.packetFilter import Packet_filter


class UDPParser:
    def __init__(self):
        self.udp_port = 20777
        self.udp_host = "0.0.0.0"
        self.udp_socket: Optional[socket.socket] = None
        self.stop_event = threading.Event()
        self.packets = Queue[bytes]()
        self.filter = Packet_filter()

    def _receiver(self):
        self.udp_socket.bind((self.udp_host, self.udp_port))
        print(f"Listening for UDP packets on port {self.udp_port}...")
        while not self.stop_event.is_set():
            try:
                data, addr = self.udp_socket.recvfrom(65507) # Buffer size is 65507 bytes
                self.packets.put(data)
                print(self.filter.motion_p)


            except socket.error as e:
                print(f"Socket error: {e}")
        print("Receiver thread is stopping...")


    def _sender(self):
        while self.udp_socket:
            self.filter.unpack_packet(self.packets.get())


    def start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        receiver_thread = threading.Thread(target=self._receiver)
        receiver_thread.daemon = True
        receiver_thread.start()

        sender_thread = threading.Thread(target=self._sender())
        sender_thread.daemon = True
        sender_thread.start()

        receiver_thread.join()
        sender_thread.join()

