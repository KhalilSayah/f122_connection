import struct


class PacketHeader:
    def __init__(self, packet_format, game_major_version, game_minor_version, packet_version, packet_id, session_uid, session_time, frame_identifier, player_car_index, secondary_player_car_index):
        self.packet_format = packet_format
        self.game_major_version = game_major_version
        self.game_minor_version = game_minor_version
        self.packet_version = packet_version
        self.packet_id = packet_id
        self.session_uid = session_uid
        self.session_time = session_time
        self.frame_identifier = frame_identifier
        self.player_car_index = player_car_index
        self.secondary_player_car_index = secondary_player_car_index

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) < 26:
            raise ValueError("Data is too short to contain a valid packet header")

        # Unpack the bytes into respective fields
        packet_format, game_major_version, game_minor_version, packet_version, packet_id = struct.unpack('!HBBBB',
                                                                                                         data[:6])
        session_uid = struct.unpack('!Q', data[6:14])[0]
        session_time = struct.unpack('!f', data[14:18])[0]
        frame_identifier = struct.unpack('!I', data[18:22])[0]
        player_car_index, secondary_player_car_index = struct.unpack('!BB', data[22:24])

        return cls(packet_format, game_major_version, game_minor_version, packet_version,
                   packet_id, session_uid, session_time, frame_identifier,
                   player_car_index, secondary_player_car_index)