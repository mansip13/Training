import psycopg2
from api_request import fetch_data

def connect_db():
    print("Connecting to db ...")
    try:   
        conn = psycopg2.connect(
            host ="db",
            port = 5432,
            dbname= "db",
            user = "db_user",
            password= "db_password"
        )
        return conn
        
    except psycopg2.Error as e:
        print(f"connection failed: {e}")
        raise

def create_table(conn):
    print("Creating table....")
    try:
        cursor=conn.cursor()
        cursor.execute(""" 
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data(
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );           
            """)
        conn.commit()
        print("Table created...")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records(conn,data):
    print("Inserting values ...")
    try: 
        weather=data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dev.raw_weather_data(
                city,
                temperature,
                weather_description,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            )VALUES(%s, %s, %s, %s, %s, NOW(), %s)
            """,(
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
            ))
        conn.commit()
        print("data insertd !")
    except psycopg2.Error as e: 
        print(f"Error inserting values: {e}")
        raise
    
    
def main():
    try: 
        data = fetch_data()        
        conn = connect_db()
        create_table(conn)
        insert_records(conn, data)    
                
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        if 'conn' in locals():
            conn.close()
            print("Database connection closed")
main()q