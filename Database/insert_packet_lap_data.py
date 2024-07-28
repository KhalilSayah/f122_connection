def insert_packet_lap_data(packet_lap_data, cursor):
    header_data = packet_lap_data["m_header"]
    cursor.execute(
        """
        INSERT INTO PacketHeader (packet_format, game_major_version, game_minor_version, packet_version, packet_id, session_uid, session_time, frame_identifier, player_car_index, secondary_player_car_index)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (header_data["packet_format"], header_data["game_major_version"], header_data["game_minor_version"],
         header_data["packet_version"], header_data["packet_id"], header_data["session_uid"],
         header_data["session_time"], header_data["frame_identifier"], header_data["player_car_index"],
         header_data["secondary_player_car_index"])
    )
    header_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO PacketLapData (packet_header_id, time_trial_pb_car_idx, time_trial_rival_car_idx)
        VALUES (%s, %s, %s) RETURNING id
        """,
        (header_id, packet_lap_data["m_timeTrialPBCarIdx"], packet_lap_data["m_timeTrialRivalCarIdx"])
    )
    packet_lap_data_id = cursor.fetchone()[0]

    for i, lap_data in enumerate(packet_lap_data["m_lapData"]):
        cursor.execute(
            """
            INSERT INTO LapData (
                packet_lap_data_id, car_index, last_lap_time_in_ms, current_lap_time_in_ms, sector1_time_in_ms, sector2_time_in_ms,
                lap_distance, total_distance, safety_car_delta, car_position, current_lap_num, pit_status, num_pit_stops,
                sector, current_lap_invalid, penalties, warnings, num_unserved_drive_through_pens, num_unserved_stop_go_pens,
                grid_position, driver_status, result_status, pit_lane_timer_active, pit_lane_time_in_lane_in_ms, pit_stop_timer_in_ms,
                pit_stop_should_serve_pen
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                packet_lap_data_id, i, lap_data["m_lastLapTimeInMS"], lap_data["m_currentLapTimeInMS"],
                lap_data["m_sector1TimeInMS"], lap_data["m_sector2TimeInMS"], lap_data["m_lapDistance"],
                lap_data["m_totalDistance"], lap_data["m_safetyCarDelta"], lap_data["m_carPosition"],
                lap_data["m_currentLapNum"], lap_data["m_pitStatus"], lap_data["m_numPitStops"], lap_data["m_sector"],
                lap_data["m_currentLapInvalid"], lap_data["m_penalties"], lap_data["m_warnings"],
                lap_data["m_numUnservedDriveThroughPens"], lap_data["m_numUnservedStopGoPens"], lap_data["m_gridPosition"],
                lap_data["m_driverStatus"], lap_data["m_resultStatus"], lap_data["m_pitLaneTimerActive"],
                lap_data["m_pitLaneTimeInLaneInMS"], lap_data["m_pitStopTimerInMS"], lap_data["m_pitStopShouldServePen"]
            )
        )
