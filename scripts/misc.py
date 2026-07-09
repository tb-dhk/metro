import sqlite3

connection = sqlite3.connect("metro.db")
cursor = connection.cursor()


def service_string_to_list(string):
    segments = string.split(", ")
    final = []
    for s in segments:
        if "..." in s:
            start = int(s.split("...")[0][-2:])
            end = int(s.split("...")[1])
            code = s.split("...")[0][:-2]
            interval = -1 if start > end else 1
            for i in range(start, end + interval, interval):
                final.append(code + str(i).rjust(2, "0"))
        else:
            final.append(s)
    return final


def list_of_service_stations(line, service):
    cursor.execute(
        """
        SELECT Stations FROM Service
        WHERE LineCode = ? AND Name = ?
    """,
        (line, service),
    )
    return service_string_to_list(cursor.fetchall()[0][0])


def get_station_from_code(code):
    if code == "none":
        return "none"
    cursor.execute(
        """
        SELECT StationName FROM StationCode
        WHERE LineCode || Number = ?
    """,
        (code,),
    )
    return cursor.fetchall()[0][0]


def surrounding_stations(station, line, service):
    cursor.execute(
        """
        SELECT LineCode || Number FROM StationCode
        WHERE StationName = ? AND LineCode = ?
    """,
        (station, line),
    )
    code = cursor.fetchall()[0][0]
    stations = list_of_service_stations(line, service)

    loop = service[-4:] == "wise"
    if loop and stations[-1] == stations[0]:
        stations.pop(-1)

    indices = [i for i in range(len(stations)) if stations[i] == code]
    if loop:
        return [
            (
                stations[(i - 1) % len(stations)],
                stations[(i + 1) % len(stations)],
            )
            for i in indices
        ]
    else:
        return [
            (
                stations[i - 1] if i > 0 else "none",
                stations[(i + 1)] if i < len(stations) - 1 else "none",
            )
            for i in indices
        ]


def end_destination(line, service):
    return list_of_service_stations(line, service)[-1]


def get_station_services(station, with_next=False):
    services = []
    for t_pe in ["city", "borough", "district"]:
        cursor.execute(
            """
            SELECT LineCode 
            FROM StationCode INNER JOIN Line ON LineCode = Line.Code
            WHERE StationName = ? AND Type = ?
        """,
            (station, t_pe),
        )
        lines = cursor.fetchall()

        if not lines:
            continue

        for i in range(2):
            placeholders = ",".join(["?"] * len(lines))
            cursor.execute(
                f"""
                SELECT Service.Name, Line.Code, Line.Name
                FROM Service INNER JOIN Line on Service.LineCode = Line.Code
                WHERE LineCode IN ({placeholders}) AND Platform = ?
            """,
                (
                    *[i[0] for i in lines],
                    i + 1,
                ),
            )
            services.append(cursor.fetchall())
    return services
