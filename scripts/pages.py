import sqlite3
import subprocess
from misc import *
from copy import deepcopy

TYPES = ["city", "borough", "district"]
LINES_PAGE_FIELDS = [
    "BoroughCode",
    "Area",
    "Line.Name",
    "Line.Code",
    "Color",
    "Notes",
]
LINES_PAGE_HEADERS = ["borough", "district", "name", "code", "color", "notes"]
INDIV_LINE_FIELDS = [
    "Borough.Name",
    "District.Name",
    "LineCode || Number",
    "Station.Name",
]
INDIV_LINE_HEADERS = ["borough", "district", "code", "other codes", "name"]


def markdownify(data, headers=[], linkify=[]):
    data = data if headers else data[1:]
    data = [list(row) for row in data]
    headers = headers if headers else data[0]
    columns = len(headers)
    string = "\n\n"
    string += "|" + "|".join(headers) + "|" + "\n"
    string += "|-" * columns + "|" + "\n"
    for i, row in enumerate(data):
        row = [str(j) for j in row]
        for j in range(len(row)):
            if headers[j] in linkify and row[j] != "none":
                row[j] = f"[[{row[j]}]]"
            if i > 0:
                last_column_value = [
                    data[r][j] for r in range(i) if data[r][j] != "^"
                ][-1]
                if str(last_column_value) in [row[j], row[j][2:-2]]:
                    row[j] = "^"
        string += "|" + "|".join(row) + "|" + "\n"
    string += "\n"
    return string


print("clearing old files...")
subprocess.run(["sudo rm -rf ../stations/*"], shell=True)

connection = sqlite3.connect("metro.db")
cursor = connection.cursor()

# list of lines page
print("updating list of lines page...")
lines_fragments = [
    """
there are three tiers of metro lines; city, borough and district. each station has up to three tracks, where trains of each tier share the same track. each line and station has a logo. this symbol is in the line color and shape. see [[graphic design|here]] for more on metro-related design.

# city
city lines travel across boroughs.
    """.strip(),
    """
# borough
borough lines travel within boroughs, but across districts.
    """.strip(),
    """
## district
each district has its own line, except for oak and maple island (only one station each) and the peninsula (only one district). district line codes are two letters.
    """.strip(),
]

lines = {}
tables = {}

for i, t_pe in enumerate(TYPES):
    specific_headers = deepcopy(LINES_PAGE_HEADERS)
    if t_pe == "city":
        specific_headers = specific_headers[2:]
        inner_join_string = ""
        sort_string = ""
    elif t_pe == "borough":
        specific_headers = specific_headers[1:]
        inner_join_string = ""
        sort_string = "ORDER BY Area ASC"
    else:
        inner_join_string = """
            INNER JOIN District ON Area = District.Code
            INNER JOIN Borough ON District.BoroughCode = Borough.Code
        """
        sort_string = "ORDER BY BoroughCode, Area ASC"

    cursor.execute(
        f"""
        SELECT {", ".join(LINES_PAGE_FIELDS[-i - 4 :])} 
        FROM Line {inner_join_string}
        WHERE Type = ? 
        {sort_string} 
    """,
        (t_pe,),
    )
    lines[t_pe] = [list(i) for i in cursor.fetchall()]
    modified = deepcopy(lines[t_pe])
    for row in modified:
        row[-3] = rf"![[assets/lines/{row[-4]}.svg\|40]]"
    tables[t_pe] = markdownify(
        modified, headers=specific_headers, linkify=["name"]
    )

lines_text = ""
for i, t_pe in enumerate(TYPES):
    lines_text += lines_fragments[i] + tables[t_pe]

with open("../list of lines.md", "w") as f:
    f.write(lines_text.strip())

# list of stations page
print("updating list of stations page...")
station_table = []
cursor.execute("""
    SELECT Borough.Name, District.Name, Station.Name 
    FROM Station INNER JOIN District ON DistrictCode = District.Code
    INNER JOIN Borough ON BoroughCode = Borough.Code
""")
stations = cursor.fetchall()
for borough, district, station in stations:
    row = [borough, district, station]
    for t_pe in TYPES:
        cursor.execute(
            """
            SELECT LineCode || Number
            FROM StationCode INNER JOIN Line ON LineCode = Line.Code
            WHERE StationName = ? AND Type = ?
        """,
            (station, t_pe),
        )
        row.append(
            "".join(
                [
                    rf"![[assets/codes/{row[0]}.svg\|100]]"
                    for row in cursor.fetchall()
                ]
            )
        )
    station_table.append(row)
with open("../list of stations.md", "w") as f:
    f.write(
        markdownify(
            sorted(station_table, key=lambda x: [x[0:2], x[5:2:-1]]),
            headers=["borough", "district", "station"]
            + [t_pe + " codes" for t_pe in TYPES],
            linkify=["station"],
        )
    )

# individual line pages
print("updating line pages...")
subprocess.run([f"sudo rm -rf ../lines/city/*"], shell=True)
subprocess.run([f"sudo rm -rf ../lines/borough/*"], shell=True)
subprocess.run([f"sudo rm -rf ../lines/district/*"], shell=True)

for i, t_pe in enumerate(TYPES):
    for line in lines[t_pe]:
        properties = {
            "code": line[-3],
            "color (hex)": line[-2][1:],
            "type": t_pe,
            "notes": line[-1],
        }
        if t_pe != "city":
            properties["borough"] = line[0]
        if t_pe == "district":
            properties["district"] = line[1]
        properties_string = (
            "---\n"
            + "\n".join([f"{k}: {v}" for k, v in properties.items()])
            + "\n---"
        )

        cursor.execute(
            f"""
            SELECT {",".join(INDIV_LINE_FIELDS[i:])}
            FROM StationCode 
            INNER JOIN Station ON StationCode.StationName = Station.Name
            INNER JOIN District ON Station.DistrictCode = District.Code
            INNER JOIN Borough ON District.BoroughCode = Borough.Code
            WHERE LineCode = ?
            ORDER BY Number ASC
        """,
            (line[i + 1],),
        )
        stations = [list(i) for i in cursor.fetchall()]
        for row in stations:
            row[-2] = rf"![[assets/codes/{row[-2]}.svg\|40]]"
            cursor.execute(
                """
                SELECT LineCode, Number 
                FROM StationCode INNER JOIN Line ON LineCode = Line.Code
                WHERE StationName = ? AND LineCode != ?
                ORDER BY CASE Type
                    WHEN 'city'   THEN 1
                    WHEN 'borough' THEN 2
                    WHEN 'district'    THEN 3
                    ELSE 4 -- Catches any other values
                END ASC
            """,
                (row[-1], line[i + 1]),
            )
            codes = cursor.fetchall()
            row.insert(
                -1,
                "".join(
                    [
                        rf"![[assets/codes/{line}{number}.svg\|40]]"
                        for line, number in codes
                    ]
                ),
            )

        stations_string = "# stations" + markdownify(
            stations, headers=INDIV_LINE_HEADERS[i:], linkify=["name"]
        )

        cursor.execute(
            """
            SELECT Name, Stations
            FROM Service
            WHERE LineCode = ?
            ORDER BY Stations ASC
        """,
            (line[i + 1],),
        )
        services = cursor.fetchall()
        services_string = "# services" + markdownify(
            services, headers=["name", "stations"]
        )

        filename = f"../lines/{t_pe}/{line[-4]}.md"
        subprocess.call(["touch", filename])
        subprocess.call(["chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(
                properties_string
                + "\n"
                + stations_string
                + "\n"
                + services_string
            )

# station pages
print("updating station pages...")
cursor.execute("""
    SELECT Borough.Name, District.Name, Station.Name
    FROM Station INNER JOIN District ON Station.DistrictCode = District.Code 
    INNER JOIN Borough ON District.BoroughCode = Borough.Code
""")
stations = cursor.fetchall()
for borough, district, station in stations:
    properties_string = f"---\nborough: {borough}\ndistrict: {district}\n---"

    lines_split = []
    for t_pe in TYPES:
        cursor.execute(
            """
            SELECT Name, LineCode || Number 
            FROM StationCode INNER JOIN Line ON LineCode = Line.Code
            WHERE StationName = ? AND Type = ?
        """,
            (station, t_pe),
        )
        lines_split.append(cursor.fetchall())
    lines_split = [i for i in lines_split if i]

    services = get_station_services(station)
    platform_data = []
    for i, platform in enumerate(services):
        for service, code, line in platform:
            surrounding = surrounding_stations(station, code, service)
            for prev, next in surrounding:
                platform_data.append(
                    [
                        i + 1,
                        line,
                        rf"![[assets/lines/{line}.svg\|40]]",
                        service,
                        get_station_from_code(prev),
                        rf"![[assets/codes/{prev}.svg\|40]]"
                        if prev != "none"
                        else "<",
                        get_station_from_code(next),
                        rf"![[assets/codes/{next}.svg\|40]]"
                        if next != "none"
                        else "<",
                    ]
                )

    platforms_string = "# services" + markdownify(
        platform_data,
        headers=[
            "platform",
            "line",
            "<",
            "service",
            "previous station",
            "<",
            "next station",
            "<",
        ],
        linkify=["line", "previous station", "next station"],
    )

    filename = f"../stations/{station}.md"
    subprocess.call(["touch", filename])
    subprocess.call(["chmod", "777", filename])
    with open(filename, "w") as f:
        f.write(
            properties_string
            + f"\n![[assets/stations/{station}.svg]]\n"
            + platforms_string
            + f"\n![[assets/navigation/{station}.svg]]"
        )

connection.close()
