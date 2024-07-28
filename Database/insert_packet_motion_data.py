import psycopg2

def insert_packet_motion_data(packet_motion_data, cursor):
    header_data = packet_motion_data["m_header"]
    cursor.execute(
        """
        INSERT INTO PacketHeader (packet_format, game_major_version, game_minor_version, packet_version, packet_id, session_uid, session_time, frame_identifier, player_car_index, secondary_player_car_index)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (header_data["packet_format"], header_data["game_major_version"], header_data["game_minor_version"], header_data["packet_version"], header_data["packet_id"], header_data["session_uid"], header_data["session_time"], header_data["frame_identifier"], header_data["player_car_index"], header_data["secondary_player_car_index"])
    )
    header_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO PacketMotionData (header_id)
        VALUES (%s) RETURNING id
        """,
        (header_id,)
    )
    packet_motion_data_id = cursor.fetchone()[0]

    for i, car_motion_data in enumerate(packet_motion_data["m_carMotionData"]):
        cursor.execute(
            """
            INSERT INTO CarMotionData (packet_motion_data_id, car_index, world_position_x, world_position_y, world_position_z, world_velocity_x, world_velocity_y, world_velocity_z, world_forward_dir_x, world_forward_dir_y, world_forward_dir_z, world_right_dir_x, world_right_dir_y, world_right_dir_z, g_force_lateral, g_force_longitudinal, g_force_vertical, yaw, pitch, roll)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (packet_motion_data_id, i, car_motion_data["m_worldPositionX"], car_motion_data["m_worldPositionY"], car_motion_data["m_worldPositionZ"], car_motion_data["m_worldVelocityX"], car_motion_data["m_worldVelocityY"], car_motion_data["m_worldVelocityZ"], car_motion_data["m_worldForwardDirX"], car_motion_data["m_worldForwardDirY"], car_motion_data["m_worldForwardDirZ"], car_motion_data["m_worldRightDirX"], car_motion_data["m_worldRightDirY"], car_motion_data["m_worldRightDirZ"], car_motion_data["m_gForceLateral"], car_motion_data["m_gForceLongitudinal"], car_motion_data["m_gForceVertical"], car_motion_data["m_yaw"], car_motion_data["m_pitch"], car_motion_data["m_roll"])
        )

    cursor.execute(
        """
        INSERT INTO SuspensionData (packet_motion_data_id, wheel_position_RL, wheel_position_RR, wheel_position_FL, wheel_position_FR, wheel_velocity_RL, wheel_velocity_RR, wheel_velocity_FL, wheel_velocity_FR, wheel_acceleration_RL, wheel_acceleration_RR, wheel_acceleration_FL, wheel_acceleration_FR)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (packet_motion_data_id, *packet_motion_data["m_suspensionPosition"], *packet_motion_data["m_suspensionVelocity"], *packet_motion_data["m_suspensionAcceleration"])
    )

    cursor.execute(
        """
        INSERT INTO WheelData (packet_motion_data_id, wheel_speed_RL, wheel_speed_RR, wheel_speed_FL, wheel_speed_FR, wheel_slip_RL, wheel_slip_RR, wheel_slip_FL, wheel_slip_FR)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (packet_motion_data_id, *packet_motion_data["m_wheelSpeed"], *packet_motion_data["m_wheelSlip"])
    )

    cursor.execute(
        """
        INSERT INTO LocalVelocityData (packet_motion_data_id, local_velocity_x, local_velocity_y, local_velocity_z)
        VALUES (%s, %s, %s, %s)
        """,
        (packet_motion_data_id, packet_motion_data["m_localVelocityX"], packet_motion_data["m_localVelocityY"], packet_motion_data["m_localVelocityZ"])
    )

    cursor.execute(
        """
        INSERT INTO AngularData (packet_motion_data_id, angular_velocity_x, angular_velocity_y, angular_velocity_z, angular_acceleration_x, angular_acceleration_y, angular_acceleration_z, front_wheels_angle)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (packet_motion_data_id, packet_motion_data["m_angularVelocityX"], packet_motion_data["m_angularVelocityY"], packet_motion_data["m_angularVelocityZ"], packet_motion_data["m_angularAccelerationX"], packet_motion_data["m_angularAccelerationY"], packet_motion_data["m_angularAccelerationZ"], packet_motion_data["m_frontWheelsAngle"])
    )
