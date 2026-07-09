import sqlite3
import os
import csv

print("clearing old database...")
if os.path.exists("metro.db"):
    os.remove("metro.db")

connection = sqlite3.connect("metro.db")
cursor = connection.cursor()

print("creating tables...")

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE Borough (
        Code TEXT PRIMARY KEY CHECK (Code IN ('1', '2', '3', '4', '5', 'P', 'I')),
        Name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE District (
        Code TEXT PRIMARY KEY CHECK (length(Code) = 2), 
        Name TEXT NOT NULL,
        BoroughCode TEXT NOT NULL,
        FOREIGN KEY (BoroughCode) REFERENCES Borough(Code)
    )
""")

cursor.execute("""
    CREATE TABLE Station (
        Name TEXT PRIMARY KEY,
        DistrictCode TEXT NOT NULL,
        Operating INTEGER CHECK (Operating IN (0, 1)),
        FOREIGN KEY (DistrictCode) REFERENCES District(Code)
    )
""")

cursor.execute("""
    CREATE TABLE Line (
        Code TEXT NOT NULL CHECK (length(Code) <= 2),
        Name TEXT NOT NULL,
        Type TEXT NOT NULL CHECK (Type IN ('city', 'borough', 'district')),
        Area TEXT NOT NULL,
        Color TEXT NOT NULL CHECK (Color LIKE '#%'),
        Notes TEXT,
        PRIMARY KEY (Code)
    )
""")

cursor.execute("""
    CREATE TABLE Service (
        Name TEXT,
        LineCode TEXT NOT NULL,
        Stations TEXT NOT NULL,
        Platform INTEGER CHECK (Platform IN (1, 2)),
        FOREIGN KEY (LineCode) REFERENCES Line(Code),
        PRIMARY KEY (Name, LineCode)
    )
""")

cursor.execute("""
    CREATE TABLE StationCode (
        LineCode TEXT NOT NULL,
        Number TEXT NOT NULL CHECK (length(Number) = 2),
        StationName TEXT NOT NULL,
        PRIMARY KEY (LineCode, Number),
        FOREIGN KEY (LineCode) REFERENCES Line(Code),
        FOREIGN KEY (StationName) REFERENCES Station(Name)
    )
""")

connection.commit()

print("tables created successfully! adding data...")

data_pipeline = [
    {
        "file": "borough.csv",
        "table": "Borough",
        "query": "INSERT INTO Borough (Code, Name) VALUES (?, ?)",
    },
    {
        "file": "district.csv",
        "table": "District",
        "query": "INSERT INTO District (Code, Name, BoroughCode) VALUES (?, ?, ?)",
    },
    {
        "file": "station.csv",
        "table": "Station",
        "query": "INSERT INTO Station (Name, DistrictCode, Operating) VALUES (?, ?, ?)",
    },
    {
        "file": "line.csv",
        "table": "Line",
        "query": "INSERT INTO Line (Code, Name, Type, Area, Color, Notes) VALUES (?, ?, ?, ?, ?, ?)",
    },
    {
        "file": "service.csv",
        "table": "Service",
        "query": "INSERT INTO Service (Name, LineCode, Stations, Platform) VALUES (?, ?, ?, ?)",
    },
    {
        "file": "stationcode.csv",
        "table": "StationCode",
        "query": "INSERT INTO StationCode (LineCode, Number, StationName) VALUES (?, ?, ?)",
    },
]

for step in data_pipeline:
    file_path = step["file"]
    table_name = step["table"]
    insert_query = step["query"]

    with open(file_path, mode="r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        data_rows = [tuple(row) for row in csv_reader]

        if data_rows:
            cursor.executemany(insert_query, data_rows)

print("data added successfully!")

connection.commit()
connection.close()
