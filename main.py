from UDP.udp_packets import UDPParser
if __name__ == '__main__':
    parser = UDPParser()
    parser.start()

    # Keep the main thread running to allow UDP reception
    #while True:
        #pass