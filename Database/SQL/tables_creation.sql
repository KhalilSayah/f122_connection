CREATE TABLE PacketHeader (
    id SERIAL PRIMARY KEY,
    packet_format SMALLINT,
    game_major_version INT,
    game_minor_version INT,
    packet_version INT,
    packet_id INT,
    session_uid BIGINT,
    session_time FLOAT,
    frame_identifier INTEGER,
    player_car_index INT,
    secondary_player_car_index INT
);

CREATE TABLE PacketMotionData (
    id SERIAL PRIMARY KEY,
    header_id INTEGER,
    FOREIGN KEY (header_id) REFERENCES PacketHeader(id)
);

CREATE TABLE CarMotionData (
    id SERIAL PRIMARY KEY,
    packet_motion_data_id INTEGER,
    car_index INT,
    world_position_x FLOAT,
    world_position_y FLOAT,
    world_position_z FLOAT,
    world_velocity_x FLOAT,
    world_velocity_y FLOAT,
    world_velocity_z FLOAT,
    world_forward_dir_x SMALLINT,
    world_forward_dir_y SMALLINT,
    world_forward_dir_z SMALLINT,
    world_right_dir_x SMALLINT,
    world_right_dir_y SMALLINT,
    world_right_dir_z SMALLINT,
    g_force_lateral FLOAT,
    g_force_longitudinal FLOAT,
    g_force_vertical FLOAT,
    yaw FLOAT,
    pitch FLOAT,
    roll FLOAT,
    FOREIGN KEY (packet_motion_data_id) REFERENCES PacketMotionData(id)
);


CREATE TABLE SuspensionData (
    id SERIAL PRIMARY KEY,
    packet_motion_data_id INTEGER,
    wheel_position_RL FLOAT,
    wheel_position_RR FLOAT,
    wheel_position_FL FLOAT,
    wheel_position_FR FLOAT,
    wheel_velocity_RL FLOAT,
    wheel_velocity_RR FLOAT,
    wheel_velocity_FL FLOAT,
    wheel_velocity_FR FLOAT,
    wheel_acceleration_RL FLOAT,
    wheel_acceleration_RR FLOAT,
    wheel_acceleration_FL FLOAT,
    wheel_acceleration_FR FLOAT,
    FOREIGN KEY (packet_motion_data_id) REFERENCES PacketMotionData(id)
);

CREATE TABLE WheelData (
    id SERIAL PRIMARY KEY,
    packet_motion_data_id INTEGER,
    wheel_speed_RL FLOAT,
    wheel_speed_RR FLOAT,
    wheel_speed_FL FLOAT,
    wheel_speed_FR FLOAT,
    wheel_slip_RL FLOAT,
    wheel_slip_RR FLOAT,
    wheel_slip_FL FLOAT,
    wheel_slip_FR FLOAT,
    FOREIGN KEY (packet_motion_data_id) REFERENCES PacketMotionData(id)
);

CREATE TABLE LocalVelocityData (
    id SERIAL PRIMARY KEY,
    packet_motion_data_id INTEGER,
    local_velocity_x FLOAT,
    local_velocity_y FLOAT,
    local_velocity_z FLOAT,
    FOREIGN KEY (packet_motion_data_id) REFERENCES PacketMotionData(id)
);

CREATE TABLE AngularData (
    id SERIAL PRIMARY KEY,
    packet_motion_data_id INTEGER,
    angular_velocity_x FLOAT,
    angular_velocity_y FLOAT,
    angular_velocity_z FLOAT,
    angular_acceleration_x FLOAT,
    angular_acceleration_y FLOAT,
    angular_acceleration_z FLOAT,
    front_wheels_angle FLOAT,
    FOREIGN KEY (packet_motion_data_id) REFERENCES PacketMotionData(id)
);

CREATE TABLE PacketLapData (
    id SERIAL PRIMARY KEY,
    packet_header_id INT REFERENCES PacketHeader(id),
    time_trial_pb_car_idx INT,
    time_trial_rival_car_idx INT
);

CREATE TABLE LapData (
    id SERIAL PRIMARY KEY,
    packet_lap_data_id INT REFERENCES PacketLapData(id),
    car_index INT,
    last_lap_time_in_ms INT,
    current_lap_time_in_ms INT,
    sector1_time_in_ms INT,
    sector2_time_in_ms INT,
    lap_distance FLOAT,
    total_distance FLOAT,
    safety_car_delta FLOAT,
    car_position INT,
    current_lap_num INT,
    pit_status INT,
    num_pit_stops INT,
    sector INT,
    current_lap_invalid INT,
    penalties INT,
    warnings INT,
    num_unserved_drive_through_pens INT,
    num_unserved_stop_go_pens INT,
    grid_position INT,
    driver_status INT,
    result_status INT,
    pit_lane_timer_active INT,
    pit_lane_time_in_lane_in_ms INT,
    pit_stop_timer_in_ms INT,
    pit_stop_should_serve_pen INT
);



