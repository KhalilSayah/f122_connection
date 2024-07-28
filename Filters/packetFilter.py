from Packets.packets import PacketHeader
from Packets.packets_classes import *
from typing import cast
import ctypes
from ctypes import create_string_buffer, cast, POINTER
from Database.connect_db import connect_db
from Database.insert_packet_motion_data import insert_packet_motion_data
from Database.insert_packet_telemetry import insert_packet_car_telemetry_data
from Database.insert_packet_lap_data import insert_packet_lap_data

from Packets.ctype_classes import Packet,CarTelemetryData, CarTelemetryPacket
class  Packet_filter:
    def __init__(self):
        self.motion_p: [PacketMotionData] = []
        self.telemetry_p: [PacketCarTelemetryData] = []
        self.lapdata_p: [PacketLapData] = []
        self.conn = connect_db()
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
            try :
                motion = PacketMotionData(data).to_dict()
                self.motion_p.append(motion)
                #self.insert_motion_data(motion)
            except:
                print("error")
                pass

        #LapDataPacket
        elif packet_id ==2:
            try :
                lapd = PacketLapData(data).to_dict()
                self.lapdata_p.append(lapd)
                #self.insert_lap_data(lapd)
            except:
                print("error")
                pass

        #TelemetryPacket
        elif packet_id ==6:
            try :
                buffer = create_string_buffer(data, ctypes.sizeof(CarTelemetryPacket))
                packet = cast(buffer, POINTER(CarTelemetryPacket)).contents
                telemetry = packet.__dict__ # Assuming you have a to_dict method or similar
                #print(telemetry)
                self.telemetry_p.append(telemetry)
                #self.insert_car_telemetry_data(telemetry)
            except:
                print("error")
                pass
        # add other later
        else:
            pass



    def insert_motion_data(self, packet):
        cursor = self.conn.cursor()
        try :
            insert_packet_motion_data(packet,cursor)
            self.conn.commit()
            print("MONTION DATA CORRECTLY INSERT ")
            cursor.close()

        except ValueError as e:
            print(f"Error parsing packet: {e}")

    def insert_lap_data(self, packet_lap_data):
        cursor = self.conn.cursor()
        try:
            insert_packet_lap_data(packet_lap_data, cursor)
            self.conn.commit()
            print("LAPDATA CORRECTLY INSERTED")
            cursor.close()
        except ValueError as e:
            print(f"Error parsing packet: {e}")

    def insert_car_telemetry_data(self, packet):
        cursor = self.conn.cursor()
        try:
            insert_packet_car_telemetry_data(packet, cursor)
            self.conn.commit()
            print("DATA CORRECTLY INSERTED")
        except ValueError as e:
            print(f"Error parsing packet: {e}")

        finally:
            cursor.close()




