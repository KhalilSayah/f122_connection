from Packets.packets import PacketHeader
from Packets.packets_classes import *

class  Packet_filter:
    def __init__(self):
        self.motion_p: [PacketMotionData] = []
        self.telemetry_p: [PacketCarTelemetryData] = []
        self.lapdata_p: [PacketLapData] = []
    def get_packet_id(self, data):
        try:
            header = PacketHeader.from_bytes(data)
            header = header.__dict__
            packet_id = header["packet_id"]
            return packet_id

        except ValueError as e:
            print(f"Error parsing packet: {e}")

    def unpack_packet(self, data):
        packet_id = self.get_packet_id(data)
        # use match instead, if we pass to 3.10
        #MotionPacket
        if packet_id == 0:
            self.motion_p.append(PacketMotionData(data).to_dict())

        #LapDataPacket
        elif packet_id ==2:
            self.lapdata_p.append(PacketLapData(data).to_dict())

        #TelemetryPacket
        elif packet_id ==6:
            self.telemetry_p.append(PacketCarTelemetryData(data).to_dict())
        # add other later
        else:
            pass


