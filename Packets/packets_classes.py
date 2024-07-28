import struct
from Packets.packets import PacketHeader
from Packets.packets_data import *
class PacketMotionData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        offset = 24
        self.m_carMotionData = []
        for _ in range(20):
            self.m_carMotionData.append(CarMotionData(data[offset:offset + CarMotionData.size()]))
            offset += CarMotionData.size()

        self.m_suspensionPosition = struct.unpack('<ffff', data[offset:offset + 4 * 4])
        offset += 4 * 4
        self.m_suspensionVelocity = struct.unpack('<ffff', data[offset:offset + 4 * 4])
        offset += 4 * 4
        self.m_suspensionAcceleration = struct.unpack('<ffff', data[offset:offset + 4 * 4])
        offset += 4 * 4
        self.m_wheelSpeed = struct.unpack('<ffff', data[offset:offset + 4 * 4])
        offset += 4 * 4
        self.m_wheelSlip = struct.unpack('<ffff', data[offset:offset + 4 * 4])
        offset += 4 * 4
        self.m_localVelocityX, self.m_localVelocityY, self.m_localVelocityZ = struct.unpack('<fff',
                                                                                            data[offset:offset + 3 * 4])
        offset += 3 * 4
        self.m_angularVelocityX, self.m_angularVelocityY, self.m_angularVelocityZ = struct.unpack('<fff', data[
                                                                                                          offset:offset + 3 * 4])
        offset += 3 * 4
        self.m_angularAccelerationX, self.m_angularAccelerationY, self.m_angularAccelerationZ = struct.unpack('<fff',
                                                                                                              data[
                                                                                                              offset:offset + 3 * 4])
        offset += 3 * 4
        self.m_frontWheelsAngle = struct.unpack('<f', data[offset:offset + 4])[0]

    def to_dict(self):
        return {
            'm_header': self.m_header.__dict__,
            'm_carMotionData': [cmd.__dict__ for cmd in self.m_carMotionData],
            'm_suspensionPosition': self.m_suspensionPosition,
            'm_suspensionVelocity': self.m_suspensionVelocity,
            'm_suspensionAcceleration': self.m_suspensionAcceleration,
            'm_wheelSpeed': self.m_wheelSpeed,
            'm_wheelSlip': self.m_wheelSlip,
            'm_localVelocityX': self.m_localVelocityX,
            'm_localVelocityY': self.m_localVelocityY,
            'm_localVelocityZ': self.m_localVelocityZ,
            'm_angularVelocityX': self.m_angularVelocityX,
            'm_angularVelocityY': self.m_angularVelocityY,
            'm_angularVelocityZ': self.m_angularVelocityZ,
            'm_angularAccelerationX': self.m_angularAccelerationX,
            'm_angularAccelerationY': self.m_angularAccelerationY,
            'm_angularAccelerationZ': self.m_angularAccelerationZ,
            'm_frontWheelsAngle': self.m_frontWheelsAngle
        }


class PacketSessionData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        offset = 24

        print(f'LEN OF SLICE DATA : {len(data[offset:offset + 21])}')

        expected_length = struct.calcsize('<B b b B H B b B H H B B B B B 21B')

        if len(data[offset:]) < expected_length:
            raise ValueError(
                f"Insufficient data length. Expected {expected_length} bytes but got {len(data[offset:])} bytes.")

        unpacked_data = struct.unpack('<B b b B H B b B H H B B B B B 21B', data[offset:offset + expected_length])
        self.m_weather = unpacked_data[0]
        self.m_trackTemperature = unpacked_data[1]
        self.m_airTemperature = unpacked_data[2]
        self.m_totalLaps = unpacked_data[3]
        self.m_trackLength = unpacked_data[4]
        self.m_sessionType = unpacked_data[5]
        self.m_trackId = unpacked_data[6]
        self.m_formula = unpacked_data[7]
        self.m_sessionTimeLeft = unpacked_data[8]
        self.m_sessionDuration = unpacked_data[9]
        self.m_pitSpeedLimit = unpacked_data[10]
        self.m_gamePaused = unpacked_data[11]
        self.m_isSpectating = unpacked_data[12]
        self.m_spectatorCarIndex = unpacked_data[13]
        self.m_sliProNativeSupport = unpacked_data[14]
        self.m_numMarshalZones = unpacked_data[15]
        offset += expected_length

        self.m_marshalZones = []
        for _ in range(self.m_numMarshalZones):
            self.m_marshalZones.append(MarshalZone(data[offset:offset + MarshalZone.size()]))
            offset += MarshalZone.size()

        expected_length = struct.calcsize('B B 56B B B 3I B B B B B B B B B B B B B B B B 2I 2B B B B')

        if len(data[offset:]) < expected_length:
            raise ValueError(
                f"2 Insufficient data length. Expected {expected_length} bytes but got {len(data[offset:])} bytes.")

        unpacked_data = struct.unpack('<B B 56B B B 3I B B B B B B B B B B B B B B B B 2I 2B B B B', data[offset:offset + expected_length])
        self.m_safetyCarStatus = unpacked_data[0]
        self.m_networkGame = unpacked_data[1]
        self.m_numWeatherForecastSamples = unpacked_data[2]
        offset += 3

        self.m_weatherForecastSamples = []
        for _ in range(self.m_numWeatherForecastSamples):
            self.m_weatherForecastSamples.append(WeatherForecastSample(data[offset:offset + WeatherForecastSample.size()]))
            offset += WeatherForecastSample.size()

        self.m_forecastAccuracy = unpacked_data[3]
        self.m_aiDifficulty = unpacked_data[4]
        self.m_seasonLinkIdentifier = unpacked_data[5]
        self.m_weekendLinkIdentifier = unpacked_data[6]
        self.m_sessionLinkIdentifier = unpacked_data[7]
        self.m_pitStopWindowIdealLap = unpacked_data[8]
        self.m_pitStopWindowLatestLap = unpacked_data[9]
        self.m_pitStopRejoinPosition = unpacked_data[10]
        self.m_steeringAssist = unpacked_data[11]
        self.m_brakingAssist = unpacked_data[12]
        self.m_gearboxAssist = unpacked_data[13]
        self.m_pitAssist = unpacked_data[14]
        self.m_pitReleaseAssist = unpacked_data[15]
        self.m_ERSAssist = unpacked_data[16]
        self.m_DRSAssist = unpacked_data[17]
        self.m_dynamicRacingLine = unpacked_data[18]
        self.m_dynamicRacingLineType = unpacked_data[19]
        self.m_gameMode = unpacked_data[20]
        self.m_ruleSet = unpacked_data[21]
        self.m_timeOfDay = unpacked_data[22]
        self.m_sessionLength = unpacked_data[23]


class PacketLapData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        offset = 24

        self.m_lapData = []
        for _ in range(20):
            lap_data = LapData(data[offset:offset + 44])
            self.m_lapData.append(lap_data)
            offset += LapData.size()

        self.m_timeTrialPBCarIdx, self.m_timeTrialRivalCarIdx = struct.unpack('<BB', data[offset:offset + 2])

    def to_dict(self):
        return {
            'm_header': self.m_header.__dict__,
            'm_lapData': [lap_data.to_dict() for lap_data in self.m_lapData],
            'm_timeTrialPBCarIdx': self.m_timeTrialPBCarIdx,
            'm_timeTrialRivalCarIdx': self.m_timeTrialRivalCarIdx
        }

class PacketEventData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_eventStringCode = data[24:28]
        self.m_eventDetails = EventDataDetails(self.m_eventStringCode, data[28:])




class PacketParticipantsData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_numActiveCars = struct.unpack('<B', data[24:25])[0]
        self.m_participants = [
            ParticipantData(data[25 + i * 56: 25 + (i + 1) * 56]) for i in range(20)
        ]


class PacketCarSetupData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_carSetups = [
            CarSetupData(data[24 + i * 49: 24 + (i + 1) * 49]) for i in range(20)
        ]


class PacketCarTelemetryData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_carTelemetryData = [
            CarTelemetryData(data[24 + i * 58: 24 + (i + 1) * 58]) for i in range(20)
        ]
        offset = 24 + 22 * 58
        self.m_mfdPanelIndex = struct.unpack('<B', data[offset:offset + 1])[0]
        self.m_mfdPanelIndexSecondaryPlayer = struct.unpack('<B', data[offset + 1:offset + 2])[0]
        self.m_suggestedGear = struct.unpack('<b', data[offset + 2:offset + 3])[0]

    def to_dict(self):
        return {
            'm_header': self.m_header.__dict__,  # Assuming PacketHeader has a to_dict method
            'm_carTelemetryData': [car_telemetry.__dict__ for car_telemetry in self.m_carTelemetryData],
            'm_mfdPanelIndex': self.m_mfdPanelIndex,
            'm_mfdPanelIndexSecondaryPlayer': self.m_mfdPanelIndexSecondaryPlayer,
            'm_suggestedGear': self.m_suggestedGear
        }

class PacketCarStatusData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_carStatusData = [
            CarStatusData(data[24 + i * 47: 24 + (i + 1) * 47]) for i in range(20)
        ]


class PacketFinalClassificationData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_numCars = data[24]
        self.m_classificationData = [
            FinalClassificationData(data[25 + i * 55: 25 + (i + 1) * 55]) for i in range(20)
        ]


class PacketLobbyInfoData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_numPlayers = data[24]
        self.m_lobbyPlayers = [
            LobbyInfoData(data[25 + i * 54: 25 + (i + 1) * 54]) for i in range(20)
        ]



class PacketCarDamageData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_carDamageData = [
            CarDamageData(data[24 + i * 43: 24 + (i + 1) * 43]) for i in range(20)
        ]


class PacketSessionHistoryData:
    def __init__(self, data: bytes):
        self.m_header = PacketHeader.from_bytes(data)
        self.m_carIdx = data[24]
        self.m_numLaps = data[25]
        self.m_numTyreStints = data[26]
        self.m_bestLapTimeLapNum = data[27]
        self.m_bestSector1LapNum = data[28]
        self.m_bestSector2LapNum = data[29]
        self.m_bestSector3LapNum = data[30]
        self.m_lapHistoryData = []
        self.m_tyreStintsHistoryData = []

        offset = 31
        for _ in range(100):
            self.m_lapHistoryData.append(LapHistoryData(data[offset:offset + 9]))
            offset += 9

        for _ in range(8):
            self.m_tyreStintsHistoryData.append(TyreStintHistoryData(data[offset:offset + 3]))
            offset += 3