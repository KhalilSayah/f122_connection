from ctypes import (c_float, c_int8, c_uint8, c_uint16, c_uint32, c_uint64)
from Packets.game import F1PacketStructure
class Packet(F1PacketStructure):
    _fields_ = [
        ('packetFormat', c_uint16),
        ('gameMajorVersion', c_uint8),
        ('gameMinorVersion', c_uint8),
        ('packetVersion', c_uint8),
        ('packetId', c_uint8),
        ('sessionUID', c_uint64),
        ('sessionTime', c_float),
        ('frameIdentifier', c_uint32),
        ('playerCarIndex', c_uint8),
        ('secondaryPlayerCarIndex', c_uint8),
    ]

class CarTelemetryData(F1PacketStructure):
    _fields_ = [
        ('speed', c_uint16),
        ('throttle', c_float),
        ('steer', c_float),
        ('brake', c_float),
        ('clutch', c_uint8),
        ('gear', c_int8),
        ('engineRPM', c_uint16),
        ('drs', c_uint8),
        ('revLightsPercent', c_uint8),
        ('revLightsBitValue', c_uint16),
        ('brakesTemperature', c_uint16 * 4),
        ('tiresSurfaceTemperature', c_uint8 * 4),
        ('tiresInnerTemperature', c_uint8 * 4),
        ('engineTemperature', c_uint16),
        ('tiresPressure', c_float * 4),
        ('surfaceType', c_uint8 * 4),
    ]

class CarTelemetryPacket(Packet):
    _fields_ = [
        ('carTelemetryData', CarTelemetryData * 22),
        ('mfdPanelIndex', c_uint8),
        ('mfdPanelIndexSecondaryPlayer', c_uint8),
        ('suggestedGear', c_int8),
    ]



