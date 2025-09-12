import psycopg2
from api_request import fetch_all_beers

def connect_db():
    print("Connecting to db ...")
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"connection failed: {e}")
        raise

def create_tables(conn):
    print("Creating tables....")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_beer_data(
                id SERIAL PRIMARY KEY,
                beer_id INT UNIQUE,
                name TEXT,
                tagline TEXT,
                first_brewed TEXT,
                description TEXT,
                image TEXT,
                abv FLOAT,
                ibu FLOAT,
                ebc FLOAT,
                ph FLOAT,
                brewers_tips TEXT,
                contributed_by TEXT,
                inserted_at TIMESTAMP DEFAULT NOW()
            );        

            CREATE TABLE IF NOT EXISTS dev.malt_ingredients (
                id SERIAL PRIMARY KEY,
                beer_id INT REFERENCES dev.raw_beer_data(beer_id),
                malt_name TEXT,
                amount_value FLOAT,
                amount_unit TEXT
            );

            CREATE TABLE IF NOT EXISTS dev.hop_ingredients (
                id SERIAL PRIMARY KEY,
                beer_id INT REFERENCES dev.raw_beer_data(beer_id),
                hop_name TEXT,
                amount_value FLOAT,
                amount_unit TEXT,
                add_stage TEXT,
                attribute TEXT
            );

            CREATE TABLE IF NOT EXISTS dev.yeast_ingredients (
                id SERIAL PRIMARY KEY,
                beer_id INT REFERENCES dev.raw_beer_data(beer_id),
                yeast_name TEXT
            );

            CREATE TABLE IF NOT EXISTS dev.food_pairings (
                id SERIAL PRIMARY KEY,
                beer_id INT REFERENCES dev.raw_beer_data(beer_id),
                pairing TEXT
            );
        """)
        conn.commit()
        print("Tables created...")
    except psycopg2.Error as e:
        print(f"Failed to create tables: {e}")
        raise

def insert_records(conn, beers):
    print("Inserting beer records ...")
    try:
        cursor = conn.cursor()
        for beer in beers:
            cursor.execute("""
                INSERT INTO dev.raw_beer_data(
                    beer_id, name, tagline, first_brewed, description,
                    image, abv, ibu, ebc, ph, brewers_tips, contributed_by, inserted_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON CONFLICT (beer_id) DO NOTHING;
            """, (
                beer["id"],
                beer["name"],
                beer["tagline"],
                beer["first_brewed"],
                beer["description"],
                beer.get("image"), 
                beer.get("abv"),
                beer.get("ibu"),
                beer.get("ebc"),
                beer.get("ph"),
                beer.get("brewers_tips"),
                beer.get("contributed_by"),
            ))
        conn.commit()
        print(f"✅ Inserted {len(beers)} beers into DB")
    except psycopg2.Error as e: 
        print(f"Error inserting values: {e}")
        raise

def insert_malt_ingredients(conn, beers):
    cursor = conn.cursor()
    for beer in beers:
        beer_id = beer["id"]
        malts = beer.get("ingredients", {}).get("malt", [])
        for malt in malts:
            cursor.execute("""
                INSERT INTO dev.malt_ingredients (beer_id, malt_name, amount_value, amount_unit)
                VALUES (%s, %s, %s, %s)
            """, (
                beer_id,
                malt.get("name"),
                malt.get("amount", {}).get("value"),
                malt.get("amount", {}).get("unit")
            ))
    conn.commit()
    print("Inserted malt ingredients.")

def insert_hop_ingredients(conn, beers):
    cursor = conn.cursor()
    for beer in beers:
        beer_id = beer["id"]
        hops = beer.get("ingredients", {}).get("hops", [])
        for hop in hops:
            cursor.execute("""
                INSERT INTO dev.hop_ingredients (beer_id, hop_name, amount_value, amount_unit, add_stage, attribute)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                beer_id,
                hop.get("name"),
                hop.get("amount", {}).get("value"),
                hop.get("amount", {}).get("unit"),
                hop.get("add"),
                hop.get("attribute")
            ))
    conn.commit()
    print("Inserted hop ingredients.")

def insert_yeast_ingredients(conn, beers):
    cursor = conn.cursor()
    for beer in beers:
        beer_id = beer["id"]
        yeast = beer.get("ingredients", {}).get("yeast")
        if yeast:
            cursor.execute("""
                INSERT INTO dev.yeast_ingredients (beer_id, yeast_name)
                VALUES (%s, %s)
            """, (beer_id, yeast))
    conn.commit()
    print("Inserted yeast ingredients.")

def insert_food_pairings(conn, beers):
    cursor = conn.cursor()
    for beer in beers:
        beer_id = beer["id"]
        pairings = beer.get("food_pairing", [])
        for pairing in pairings:
            cursor.execute("""
                INSERT INTO dev.food_pairings (beer_id, pairing)
                VALUES (%s, %s)
            """, (beer_id, pairing))
    conn.commit()
    print("Inserted food pairings.")

def main():
    try: 
        beers = fetch_all_beers()
        print(f"Fetched {len(beers)} beers from API")
        
        conn = connect_db()
        create_tables(conn)
        insert_records(conn, beers)
        insert_malt_ingredients(conn, beers)
        insert_hop_ingredients(conn, beers)
        insert_yeast_ingredients(conn, beers)
        insert_food_pairings(conn, beers)
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        if 'conn' in locals():
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
