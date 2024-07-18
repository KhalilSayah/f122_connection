import struct

class CarMotionData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<fff fff hhh hhh fff fff', data)
        self.m_worldPositionX = unpacked_data[0]
        self.m_worldPositionY = unpacked_data[1]
        self.m_worldPositionZ = unpacked_data[2]
        self.m_worldVelocityX = unpacked_data[3]
        self.m_worldVelocityY = unpacked_data[4]
        self.m_worldVelocityZ = unpacked_data[5]
        self.m_worldForwardDirX = unpacked_data[6]
        self.m_worldForwardDirY = unpacked_data[7]
        self.m_worldForwardDirZ = unpacked_data[8]
        self.m_worldRightDirX = unpacked_data[9]
        self.m_worldRightDirY = unpacked_data[10]
        self.m_worldRightDirZ = unpacked_data[11]
        self.m_gForceLateral = unpacked_data[12]
        self.m_gForceLongitudinal = unpacked_data[13]
        self.m_gForceVertical = unpacked_data[14]
        self.m_yaw = unpacked_data[15]
        self.m_pitch = unpacked_data[16]
        self.m_roll = unpacked_data[17]

    @classmethod
    def size(cls):
        return struct.calcsize('<fff fff hhh hhh fff fff')


class MarshalZone:
    def __init__(self, data):
        self.m_zoneStart, self.m_zoneFlag = struct.unpack('<f b', data)

    @staticmethod
    def size():
        return struct.calcsize('<f b')

# Define WeatherForecastSample structure
class WeatherForecastSample:
    def __init__(self, data):
        self.m_sessionType, self.m_timeOffset, self.m_weather, \
        self.m_trackTemperature, self.m_trackTemperatureChange, \
        self.m_airTemperature, self.m_airTemperatureChange, \
        self.m_rainPercentage = struct.unpack('<B B B b b b b B', data)

    @staticmethod
    def size():
        return struct.calcsize('<B B B b b b b B')


class LapData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<IIHHf f f B B B B B B B B B B B B B B B H H B', data)
        self.m_lastLapTimeInMS = unpacked_data[0]
        self.m_currentLapTimeInMS = unpacked_data[1]
        self.m_sector1TimeInMS = unpacked_data[2]
        self.m_sector2TimeInMS = unpacked_data[3]
        self.m_lapDistance = unpacked_data[4]
        self.m_totalDistance = unpacked_data[5]
        self.m_safetyCarDelta = unpacked_data[6]
        self.m_carPosition = unpacked_data[7]
        self.m_currentLapNum = unpacked_data[8]
        self.m_pitStatus = unpacked_data[9]
        self.m_numPitStops = unpacked_data[10]
        self.m_sector = unpacked_data[11]
        self.m_currentLapInvalid = unpacked_data[12]
        self.m_penalties = unpacked_data[13]
        self.m_warnings = unpacked_data[14]
        self.m_numUnservedDriveThroughPens = unpacked_data[15]
        self.m_numUnservedStopGoPens = unpacked_data[16]
        self.m_gridPosition = unpacked_data[17]
        self.m_driverStatus = unpacked_data[18]
        self.m_resultStatus = unpacked_data[19]
        self.m_pitLaneTimerActive = unpacked_data[20]
        self.m_pitLaneTimeInLaneInMS = unpacked_data[21]
        self.m_pitStopTimerInMS = unpacked_data[22]
        self.m_pitStopShouldServePen = unpacked_data[23]

    @classmethod
    def size(cls):
        return struct.calcsize('<IIHHf f f B B B B B B B B B B B B B B B H H B')


class FastestLap:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<Bf', data[:5])
        self.vehicleIdx = unpacked_data[0]
        self.lapTime = unpacked_data[1]

class Retirement:
    def __init__(self, data: bytes):
        self.vehicleIdx = struct.unpack('<B', data[:1])[0]

class TeamMateInPits:
    def __init__(self, data: bytes):
        self.vehicleIdx = struct.unpack('<B', data[:1])[0]

class RaceWinner:
    def __init__(self, data: bytes):
        self.vehicleIdx = struct.unpack('<B', data[:1])[0]

class Penalty:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBBBBBB', data[:7])
        self.penaltyType = unpacked_data[0]
        self.infringementType = unpacked_data[1]
        self.vehicleIdx = unpacked_data[2]
        self.otherVehicleIdx = unpacked_data[3]
        self.time = unpacked_data[4]
        self.lapNum = unpacked_data[5]
        self.placesGained = unpacked_data[6]

class SpeedTrap:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BfBBBf', data[:12])
        self.vehicleIdx = unpacked_data[0]
        self.speed = unpacked_data[1]
        self.isOverallFastestInSession = unpacked_data[2]
        self.isDriverFastestInSession = unpacked_data[3]
        self.fastestVehicleIdxInSession = unpacked_data[4]
        self.fastestSpeedInSession = unpacked_data[5]

class StartLights:
    def __init__(self, data: bytes):
        self.numLights = struct.unpack('<B', data[:1])[0]

class DriveThroughPenaltyServed:
    def __init__(self, data: bytes):
        self.vehicleIdx = struct.unpack('<B', data[:1])[0]

class StopGoPenaltyServed:
    def __init__(self, data: bytes):
        self.vehicleIdx = struct.unpack('<B', data[:1])[0]

class Flashback:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<If', data[:8])
        self.flashbackFrameIdentifier = unpacked_data[0]
        self.flashbackSessionTime = unpacked_data[1]

class Buttons:
    def __init__(self, data: bytes):
        self.m_buttonStatus = struct.unpack('<I', data[:4])[0]

class EventDataDetails:
    def __init__(self, event_string_code: bytes, data: bytes):
        self.event_string_code = event_string_code.decode('utf-8')
        if self.event_string_code == 'FTLP':
            self.details = FastestLap(data)
        elif self.event_string_code == 'RTMT':
            self.details = Retirement(data)
        elif self.event_string_code == 'TMPT':
            self.details = TeamMateInPits(data)
        elif self.event_string_code == 'RCWN':
            self.details = RaceWinner(data)
        elif self.event_string_code == 'PENA':
            self.details = Penalty(data)
        elif self.event_string_code == 'SPTP':
            self.details = SpeedTrap(data)
        elif self.event_string_code == 'STLG':
            self.details = StartLights(data)
        elif self.event_string_code == 'DTSV':
            self.details = DriveThroughPenaltyServed(data)
        elif self.event_string_code == 'SGSV':
            self.details = StopGoPenaltyServed(data)
        elif self.event_string_code == 'FLBK':
            self.details = Flashback(data)
        elif self.event_string_code == 'BUTN':
            self.details = Buttons(data)
        else:
            self.details = None


class ParticipantData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBBBBBBB48sB', data[:56])
        self.m_aiControlled = unpacked_data[0]
        self.m_driverId = unpacked_data[1]
        self.m_networkId = unpacked_data[2]
        self.m_teamId = unpacked_data[3]
        self.m_myTeam = unpacked_data[4]
        self.m_raceNumber = unpacked_data[5]
        self.m_nationality = unpacked_data[6]
        self.m_name = unpacked_data[7].decode('utf-8').rstrip('\0')
        self.m_yourTelemetry = unpacked_data[8]


class CarSetupData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBBBffffBBBBBBBBfffffBf', data[:49])
        self.m_frontWing = unpacked_data[0]
        self.m_rearWing = unpacked_data[1]
        self.m_onThrottle = unpacked_data[2]
        self.m_offThrottle = unpacked_data[3]
        self.m_frontCamber = unpacked_data[4]
        self.m_rearCamber = unpacked_data[5]
        self.m_frontToe = unpacked_data[6]
        self.m_rearToe = unpacked_data[7]
        self.m_frontSuspension = unpacked_data[8]
        self.m_rearSuspension = unpacked_data[9]
        self.m_frontAntiRollBar = unpacked_data[10]
        self.m_rearAntiRollBar = unpacked_data[11]
        self.m_frontSuspensionHeight = unpacked_data[12]
        self.m_rearSuspensionHeight = unpacked_data[13]
        self.m_brakePressure = unpacked_data[14]
        self.m_brakeBias = unpacked_data[15]
        self.m_rearLeftTyrePressure = unpacked_data[16]
        self.m_rearRightTyrePressure = unpacked_data[17]
        self.m_frontLeftTyrePressure = unpacked_data[18]
        self.m_frontRightTyrePressure = unpacked_data[19]
        self.m_ballast = unpacked_data[20]
        self.m_fuelLoad = unpacked_data[21]


class CarTelemetryData:
    def __init__(self, data: bytes):
        #expected_length = struct.calcsize('<HffffBbhBBHHHHHHHffffBBBB')
        #print(f'expected_length : {expected_length}')
        #print(f'real_data : {len(data)}')


        unpacked_data = struct.unpack('<HffffBbhBBHHHHHHHffffBBBB', data)
        self.m_speed = unpacked_data[0]
        self.m_throttle = unpacked_data[1]
        self.m_steer = unpacked_data[2]
        self.m_brake = unpacked_data[3]
        self.m_clutch = unpacked_data[4]
        self.m_gear = unpacked_data[5]
        self.m_engineRPM = unpacked_data[6]
        self.m_drs = unpacked_data[7]
        self.m_revLightsPercent = unpacked_data[8]
        self.m_revLightsBitValue = unpacked_data[9]
        self.m_brakesTemperature = unpacked_data[10:14]
        self.m_tyresSurfaceTemperature = unpacked_data[14:18]
        self.m_tyresInnerTemperature = unpacked_data[18:22]
        self.m_engineTemperature = unpacked_data[22]
        self.m_tyresPressure = unpacked_data[23:27]
        self.m_surfaceType = unpacked_data[27:31]

    def to_dict(self):
        return {
            'm_speed': self.m_speed,
            'm_throttle': self.m_throttle,
            'm_steer': self.m_steer,
            'm_brake': self.m_brake,
            'm_clutch': self.m_clutch,
            'm_gear': self.m_gear,
            'm_engineRPM': self.m_engineRPM,
            'm_drs': self.m_drs,
            'm_revLightsPercent': self.m_revLightsPercent,
            'm_revLightsBitValue': self.m_revLightsBitValue,
            'm_brakesTemperature': self.m_brakesTemperature,
            'm_tyresSurfaceTemperature': self.m_tyresSurfaceTemperature,
            'm_tyresInnerTemperature': self.m_tyresInnerTemperature,
            'm_engineTemperature': self.m_engineTemperature,
            'm_tyresPressure': self.m_tyresPressure,
            'm_surfaceType': self.m_surfaceType
        }

class CarStatusData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBBBBffffHHBBHBBbffffB', data)
        self.m_tractionControl = unpacked_data[0]
        self.m_antiLockBrakes = unpacked_data[1]
        self.m_fuelMix = unpacked_data[2]
        self.m_frontBrakeBias = unpacked_data[3]
        self.m_pitLimiterStatus = unpacked_data[4]
        self.m_fuelInTank = unpacked_data[5]
        self.m_fuelCapacity = unpacked_data[6]
        self.m_fuelRemainingLaps = unpacked_data[7]
        self.m_maxRPM = unpacked_data[8]
        self.m_idleRPM = unpacked_data[9]
        self.m_maxGears = unpacked_data[10]
        self.m_drsAllowed = unpacked_data[11]
        self.m_drsActivationDistance = unpacked_data[12]
        self.m_actualTyreCompound = unpacked_data[13]
        self.m_visualTyreCompound = unpacked_data[14]
        self.m_tyresAgeLaps = unpacked_data[15]
        self.m_vehicleFiaFlags = unpacked_data[16]
        self.m_ersStoreEnergy = unpacked_data[17]
        self.m_ersDeployMode = unpacked_data[18]
        self.m_ersHarvestedThisLapMGUK = unpacked_data[19]
        self.m_ersHarvestedThisLapMGUH = unpacked_data[20]
        self.m_ersDeployedThisLap = unpacked_data[21]
        self.m_networkPaused = unpacked_data[22]


class FinalClassificationData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBBBBBBBBBIIdBB8B8B', data)
        self.m_position = unpacked_data[0]
        self.m_numLaps = unpacked_data[1]
        self.m_gridPosition = unpacked_data[2]
        self.m_points = unpacked_data[3]
        self.m_numPitStops = unpacked_data[4]
        self.m_resultStatus = unpacked_data[5]
        self.m_bestLapTimeInMS = unpacked_data[6]
        self.m_totalRaceTime = unpacked_data[7]
        self.m_penaltiesTime = unpacked_data[8]
        self.m_numPenalties = unpacked_data[9]
        self.m_numTyreStints = unpacked_data[10]
        self.m_tyreStintsActual = list(unpacked_data[11:19])
        self.m_tyreStintsVisual = list(unpacked_data[19:27])
        self.m_tyreStintsEndLaps = list(unpacked_data[27:35])


class LobbyInfoData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBB48sBB', data)
        self.m_aiControlled = unpacked_data[0]
        self.m_teamId = unpacked_data[1]
        self.m_nationality = unpacked_data[2]
        self.m_name = unpacked_data[3].decode('utf-8').rstrip('\x00')  # Remove null terminators
        self.m_carNumber = unpacked_data[4]
        self.m_readyStatus = unpacked_data[5]



class CarDamageData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<4f4B3BBBBBB6BBBBB', data)
        self.m_tyresWear = unpacked_data[0:4]
        self.m_tyresDamage = unpacked_data[4:8]
        self.m_brakesDamage = unpacked_data[8:12]
        self.m_frontLeftWingDamage = unpacked_data[12]
        self.m_frontRightWingDamage = unpacked_data[13]
        self.m_rearWingDamage = unpacked_data[14]
        self.m_floorDamage = unpacked_data[15]
        self.m_diffuserDamage = unpacked_data[16]
        self.m_sidepodDamage = unpacked_data[17]
        self.m_drsFault = unpacked_data[18]
        self.m_ersFault = unpacked_data[19]
        self.m_gearBoxDamage = unpacked_data[20]
        self.m_engineDamage = unpacked_data[21]
        self.m_engineMGUHWear = unpacked_data[22]
        self.m_engineESWear = unpacked_data[23]
        self.m_engineCEWear = unpacked_data[24]
        self.m_engineICEWear = unpacked_data[25]
        self.m_engineMGUKWear = unpacked_data[26]
        self.m_engineTCWear = unpacked_data[27]
        self.m_engineBlown = unpacked_data[28]
        self.m_engineSeized = unpacked_data[29]

class LapHistoryData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<IHHH B', data)
        self.m_lapTimeInMS = unpacked_data[0]
        self.m_sector1TimeInMS = unpacked_data[1]
        self.m_sector2TimeInMS = unpacked_data[2]
        self.m_sector3TimeInMS = unpacked_data[3]
        self.m_lapValidBitFlags = unpacked_data[4]

class TyreStintHistoryData:
    def __init__(self, data: bytes):
        unpacked_data = struct.unpack('<BBB', data)
        self.m_endLap = unpacked_data[0]
        self.m_tyreActualCompound = unpacked_data[1]
        self.m_tyreVisualCompound = unpacked_data[2]