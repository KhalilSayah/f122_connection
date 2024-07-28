import psycopg2

def connect_db ():
    conn = psycopg2.connect(
        dbname = "f122_telemetry",
        user = "postgres",
        password = "    ",
        host = "localhost",
        port = "5432"
    )
    return conn
