import socket
import time
import pickle


def load_packets(filename='packets.pkl'):
    with open(filename, 'rb') as file:
        packets = pickle.load(file)
    return packets


def udp_server(host="0.0.0.0", port=20777, packets=None):
    if packets is None:
        packets = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_address = (host, port)

    try:
        for packet in packets:
            server_socket.sendto(packet, client_address)
            print(f"Sent: {packet}")
            time.sleep(1)  # Send data every second
    finally:
        server_socket.close()


if __name__ == "__main__":
    packets = load_packets()
    udp_server(packets=packets)
