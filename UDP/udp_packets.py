import socket
from typing import Optional
import threading
import json
import signal
from Packets.packets import PacketHeader
from Packets.packets_classes import *


class UDPParser:
    def __init__(self):
        self.dataList: list = []
        self.udp_port = 20777
        self.udp_host = "0.0.0.0"
        self.udp_socket: Optional[socket.socket] = None
        self.stop_event = threading.Event()

    def _receiver(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.udp_host, self.udp_port))
        print(f"Listening for UDP packets on port {self.udp_port}...")
        while not self.stop_event.is_set():
            try:
                data, addr = self.udp_socket.recvfrom(65507)  # Buffer size is 65507 bytes
                packet_id = self.parse_packet(data)

                if packet_id == 6:
                    packet = PacketCarTelemetryData(data)
                    self.dataList.append(packet.to_dict())
                    # print(packet.to_dict())
                    # print("//////////////////////////////")

                # self.dataList.append(data)
            except socket.error as e:
                print(f"Socket error: {e}")
        print("Receiver thread is stopping...")

    def export_data_on_input(self):
        input("Press Enter to export data to JSON and stop all threads...\n")
        with open('exported_data.json', 'w') as f:
            json.dump(self.dataList, f, indent=4)
        print("Data exported to exported_data.json")
        self.stop_event.set()  # Signal all threads to stop

        # Close the UDP socket
        if self.udp_socket:
            self.udp_socket.close()

    def start(self):
        receiver_thread = threading.Thread(target=self._receiver)
        receiver_thread.daemon = True
        receiver_thread.start()

        input_thread = threading.Thread(target=self.export_data_on_input)
        input_thread.daemon = True
        input_thread.start()

        # Wait for threads to complete
        input_thread.join()
        receiver_thread.join()

    def get_data(self):
        return self.dataList

    def parse_packet(self, data):
        try:
            header = PacketHeader.from_bytes(data)
            header = header.__dict__
            packet_id = header["packet_id"]
            return packet_id

        except ValueError as e:
            print(f"Error parsing packet: {e}")