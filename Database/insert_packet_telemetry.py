import psycopg2

def insert_packet_car_telemetry_data(packet_telemetry_data, cursor):
    header_data = packet_telemetry_data["m_header"]

    cursor.execute(
        """
        INSERT INTO PacketHeader (
            packet_format, game_major_version, game_minor_version, packet_version, packet_id, session_uid,
            session_time, frame_identifier, player_car_index, secondary_player_car_index
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (
            header_data["packet_format"], header_data["game_major_version"], header_data["game_minor_version"],
            header_data["packet_version"], header_data["packet_id"], header_data["session_uid"],
            header_data["session_time"], header_data["frame_identifier"], header_data["player_car_index"],
            header_data["secondary_player_car_index"]
        )
    )
    header_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO PacketCarTelemetryData (
            packet_header_id, mfd_panel_index, mfd_panel_index_secondary_player, suggested_gear
        ) VALUES (%s, %s, %s, %s) RETURNING id
        """,
        (header_id, packet_telemetry_data["m_mfdPanelIndex"], packet_telemetry_data["m_mfdPanelIndexSecondaryPlayer"],
         packet_telemetry_data["m_suggestedGear"])
    )
    packet_car_telemetry_data_id = cursor.fetchone()[0]

    for i, car_telemetry_data in enumerate(packet_telemetry_data["m_carTelemetryData"]):
        # Debugging prints to check data structure
        print(f"Car telemetry data for car index {i}: {car_telemetry_data}")

        # Ensure lists have correct lengths or fill with defaults
        m_brakesTemperature = list(car_telemetry_data.get("m_brakesTemperature", [0] * 4))
        m_tyresSurfaceTemperature = list(car_telemetry_data.get("m_tyresSurfaceTemperature", [0] * 4))
        m_tyresInnerTemperature = list(car_telemetry_data.get("m_tyresInnerTemperature", [0] * 4))
        m_tyresPressure = list(car_telemetry_data.get("m_tyresPressure", [0] * 4))
        m_surfaceType = list(car_telemetry_data.get("m_surfaceType", [0] * 4))

        # Extend lists to ensure they have exactly 4 elements
        m_brakesTemperature.extend([0] * (4 - len(m_brakesTemperature)))
        m_tyresSurfaceTemperature.extend([0] * (4 - len(m_tyresSurfaceTemperature)))
        m_tyresInnerTemperature.extend([0] * (4 - len(m_tyresInnerTemperature)))
        m_tyresPressure.extend([0] * (4 - len(m_tyresPressure)))
        m_surfaceType.extend([0] * (4 - len(m_surfaceType)))

        cursor.execute(
            """
            INSERT INTO CarTelemetryData (
                packet_car_telemetry_data_id, car_index, speed, throttle, steer, brake, clutch, gear, engine_rpm, drs,
                rev_lights_percent, rev_lights_bit_value, brakes_temperature_0, brakes_temperature_1, brakes_temperature_2,
                brakes_temperature_3, tyres_surface_temperature_0, tyres_surface_temperature_1, tyres_surface_temperature_2,
                tyres_surface_temperature_3, tyres_inner_temperature_0, tyres_inner_temperature_1, tyres_inner_temperature_2,
                tyres_inner_temperature_3, engine_temperature, tyres_pressure_0, tyres_pressure_1, tyres_pressure_2,
                tyres_pressure_3, surface_type_0, surface_type_1, surface_type_2, surface_type_3
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                packet_car_telemetry_data_id, i, car_telemetry_data["m_speed"], car_telemetry_data["m_throttle"],
                car_telemetry_data["m_steer"], car_telemetry_data["m_brake"], car_telemetry_data["m_clutch"],
                car_telemetry_data["m_gear"], car_telemetry_data["m_engineRPM"], car_telemetry_data["m_drs"],
                car_telemetry_data["m_revLightsPercent"], car_telemetry_data["m_revLightsBitValue"],
                m_brakesTemperature[0], m_brakesTemperature[1], m_brakesTemperature[2], m_brakesTemperature[3],
                m_tyresSurfaceTemperature[0], m_tyresSurfaceTemperature[1], m_tyresSurfaceTemperature[2],
                m_tyresSurfaceTemperature[3], m_tyresInnerTemperature[0], m_tyresInnerTemperature[1],
                m_tyresInnerTemperature[2], m_tyresInnerTemperature[3], car_telemetry_data["m_engineTemperature"],
                m_tyresPressure[0], m_tyresPressure[1], m_tyresPressure[2], m_tyresPressure[3],
                m_surfaceType[0], m_surfaceType[1], m_surfaceType[2], m_surfaceType[3]
            )
        )
