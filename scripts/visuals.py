import svg
import sqlite3
import subprocess
import base64
import math
from misc import *

print("clearing old assets...")
subprocess.run(["sudo rm -rf ../assets/*"], shell=True)
connection = sqlite3.connect("metro.db")
cursor = connection.cursor()


def shape(t_pe, fill):
    r = 60
    if t_pe == "city":
        return svg.Circle(cx=100, cy=100, r=100, fill=fill)
    elif t_pe == "borough":
        scale = 200 / ((200 - 2 * r) * 2**0.5 + 2 * r)
        return (
            svg.Rect(
                x=100 * (1 - scale),
                y=100 * (1 - scale),
                rx=r * scale,
                ry=r * scale,
                width=200 * scale,
                height=200 * scale,
                fill=fill,
                transform="rotate(45, 100, 100)",
            ),
        )
    else:
        return svg.Rect(
            x=0,
            y=0,
            rx=r,
            ry=r,
            width=200,
            height=200,
            fill=fill,
        )


def href(filename):
    with open(filename, "rb") as f:
        return (
            f"data:image/svg+xml;base64,{base64.b64encode(f.read()).decode()}"
        )


def html_with_station(text, station=None, right=False):
    if station:
        name, code = station
        station_text = f"""
        <span>{text} {name}</span>
        <img src="{href(f"../assets/codes/{code}.svg")}" style="height: 100px; width: auto;" />
        """
    else:
        station_text = "ends here"
    return f"""
    <div xmlns="http://www.w3.org/1999/xhtml" 
         style="display: flex; 
                align-items: center; 
                justify-content: {"flex-end" if right else "flex-start"};
                gap: 25px; 
                font-family: 'Altone', sans-serif; 
                font-size: 65px; 
                font-weight: 500; 
                color: white; 
                white-space: nowrap;
                height: 100%;">
         {station_text}
    </div>
    """


def html_line_service(name, service):
    station_text = f"""
    <img src="{href(f"../assets/lines/{name}.svg")}" style="height: 100px; width: auto;" />
    <span>{name} - {service}</span>
    """
    return f"""
    <div xmlns="http://www.w3.org/1999/xhtml" 
         style="display: flex; 
                align-items: center; 
                justify-content: center;
                gap: 25px; 
                font-family: 'Altone', sans-serif; 
                font-size: 65px; 
                font-weight: 500; 
                color: white; 
                white-space: nowrap;
                height: 100%;">
         {station_text}
    </div>
    """

def html_station_name(name, current_station, blur):
    return f"""
    <div xmlns="http://www.w3.org/1999/xhtml" 
         style="
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 50px;
                padding: 10px 20px;
                font-family: 'Altone', sans-serif;
                font-size: 65px;
                font-weight: 500;
                white-space: nowrap;
                color: {"grey" if blur else "black" if name == current_station else "white"}; 
                background-color: {"white" if name == current_station else "black"};"
            >
         {name}
    </div>
    """


def line_logos():
    print("making line logos...")
    cursor.execute("""
        SELECT Name, Code, Color, Type
        FROM Line
    """)
    lines = cursor.fetchall()

    subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/lines"])
    for name, code, color, t_pe in lines:
        drawing = svg.SVG(
            width=200,
            height=200,
            elements=[
                shape(t_pe, color),
                svg.Text(
                    text=code,
                    x=100,
                    y=105,
                    text_anchor="middle",
                    dominant_baseline="middle",
                    font_size="90px",
                    fill="white",
                    font_family="Altone",
                    font_weight=700,
                ),
            ],
        )

        filename = f"../assets/lines/{name}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(drawing))


def station_codes():
    print("making station codes...")
    cursor.execute("""
        SELECT Number, LineCode, Color, Type
        FROM StationCode INNER JOIN Line ON StationCode.LineCode = Line.Code
    """)
    codes = cursor.fetchall()

    subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/codes"])
    for number, line, color, t_pe in codes:
        drawing = svg.SVG(
            width=200,
            height=200,
            elements=[
                shape(t_pe, color),
                svg.Text(
                    text=line,
                    x=100,
                    y=95,
                    text_anchor="middle",
                    font_size="85px",
                    fill="white",
                    font_family="Altone",
                    font_weight=700,
                ),
                svg.Text(
                    text=number.ljust(2, "0"),
                    x=100,
                    y=165,
                    text_anchor="middle",
                    font_size="60px",
                    fill="white",
                    font_family="Altone",
                    font_weight=700,
                ),
            ],
        )

        filename = f"../assets/codes/{line}{number.ljust(2, '0')}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(drawing))


def platform_logos():
    print("making platform logos...")
    subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/platforms"])
    for i in range(6):
        number = i + 1

        drawing = svg.SVG(
            width=200,
            height=200,
            elements=[
                svg.Rect(x=0, y=0, width=200, height=200, fill="white"),
                svg.Rect(x=25, y=25, width=150, height=150, fill="black"),
                svg.Text(
                    text=number,
                    x=100,
                    y=105,
                    text_anchor="middle",
                    dominant_baseline="middle",
                    font_size="110px",
                    fill="white",
                    font_family="Altone",
                    font_weight=700,
                ),
            ],
        )

        filename = f"../assets/platforms/{number}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(drawing))

def blurred(i, station_info, service_name, current_station):
    if i < 0 and "wise" not in service_name:
        return True
    if i >= len(station_info) and "wise" in service_name and blurred(i-1, station_info, service_name, current_station):
        return True
    if not current_station:
        return False
    if i not in range(len(station_info)):
        return False
    length = len(station_info)
    if "wise" in service_name:
        return current_station not in [station_info[(i - j) % length][1] for j in range(length // 2 + 1)]
    else:
        return i < [j for j in range(length) if station_info[j][1] == current_station][0] 

subprocess.call(["mkdir", "-p", "../assets/service_maps/general"])

def service_map(name, line, stations, color, current_station=None):
    station_list = service_string_to_list(stations)

    placeholders = ",".join(["?" for _ in station_list])
    cursor.execute(
        f"""
        SELECT COUNT(*) AS total_freq
        FROM StationCode
        WHERE StationName IN (
            SELECT StationName
            FROM StationCode
            WHERE LineCode || Number IN ({placeholders})
        )
        GROUP BY StationName
        ORDER BY total_freq DESC;
    """,
        station_list,
    )
    height = cursor.fetchone()[0]

    station_names = []
    for code in station_list:
        cursor.execute(
            """
            SELECT StationName
            FROM StationCode WHERE LineCode || Number = ?
        """,
            (code,),
        )
        station_names.append(cursor.fetchone()[0])

    
    station_info = list(zip(station_list, station_names))
    if "wise" in name:
        station_info = station_info[:-1]
        if current_station:
            index = station_names.index(current_station)
            station_info = station_info[index:] + station_info[:index]
    length = len(station_info)

    into_blur = svg.LinearGradient(
        id="into_blur", 
        x1="0%",
        y1="0%",
        x2="100%",
        y2="0%",
        elements=[
            svg.Stop(offset="0%", stop_color="#00000000"),
            svg.Stop(offset="25%", stop_color="#00000040"),
            svg.Stop(offset="100%", stop_color="#00000080"),
        ],
    )
    outof_blur = svg.LinearGradient(
        id="outof_blur", 
        x1="100%",
        y1="0%",
        x2="0%",
        y2="0%",
        elements=[
            svg.Stop(offset="0%", stop_color="#00000000"),
            svg.Stop(offset="75%", stop_color="#00000040"),
            svg.Stop(offset="100%", stop_color="#00000080"),
        ],
    )
    inandoutof_blur = svg.LinearGradient(
        id="inandoutof_blur", 
        x1="0%",
        y1="0%",
        x2="100%",
        y2="0%",
        elements=[
            svg.Stop(offset="0%", stop_color="#00000000"),
            svg.Stop(offset="10%", stop_color="#00000080"),
            svg.Stop(offset="90%", stop_color="#00000080"),
            svg.Stop(offset="100%", stop_color="#00000000"),
        ],
    )
    return_blur = svg.LinearGradient(
        id="return_blur", 
        x1="0%",
        y1="100%",
        x2="100%",
        y2="0%",
        elements=[
            svg.Stop(offset="0%", stop_color="#00000080"),
            svg.Stop(offset="25%", stop_color="#00000080"),
            svg.Stop(offset="75%", stop_color="#00000000"),
            svg.Stop(offset="100%", stop_color="#00000000"),
        ],
    )

    full_width = 300 * length + 1400
    full_height = 200 * height + 1300 
    elements = [
        svg.Defs(elements=[into_blur, outof_blur, inandoutof_blur, return_blur]),
        svg.Rect(
            x=0,
            y=0,
            width=full_width,
            height=full_height,
            fill="black",
        ),
        svg.ForeignObject(
            x=0,
            y=full_height - 300,
            width=full_width,
            height=200,
            text=html_line_service(line, name),
        ),
    ]

    if "wise" in name:
        elements += [
            svg.Rect(
                x=550,
                y=700,
                width=full_width - 1100,
                height=full_height - 1100,
                fill="black",
                style=f"stroke: {color}; stroke-width: 20px",
                rx=20,
                ry=20
            ),
            svg.Rect(
                x=(full_width - 40) / 2,
                y=full_height - 410,
                width=40 * 2 ** 0.5,
                height=20,
                fill=color,
                rx=10,
                ry=10,
                transform=f"rotate(-45 {(full_width - 40) / 2} {full_height - 400})"
            ),
            svg.Rect(
                x=(full_width - 40) / 2,
                y=full_height - 410,
                width=40 * 2 ** 0.5,
                height=20,
                fill=color,
                rx=10,
                ry=10,
                transform=f"rotate(45 {(full_width - 40) / 2} {full_height - 400})"
            ),
        ]
    else:
        elements.append(
            svg.Rect(
                x=750,
                y=690,
                width=full_width - 1700,
                height=20,
                fill=color,
            )
        )

    for i, (station_code, station_name) in enumerate(station_info):
        blur = blurred(i, station_info, name, current_station)

        cursor.execute(
            """
            SELECT sc2.LineCode || sc2.Number
            FROM StationCode sc1
            INNER JOIN StationCode sc2 ON sc1.StationName = sc2.StationName
            INNER JOIN Line ON sc2.LineCode = Line.Code
            WHERE sc1.LineCode || sc1.Number = ?
            AND sc1.LineCode || sc1.Number != sc2.LineCode || sc2.Number
            ORDER BY CASE Line.Type
                WHEN 'city'   THEN 1
                WHEN 'borough' THEN 2
                WHEN 'district'    THEN 3
                ELSE 4 -- Catches any other values
            END ASC
        """,
            (station_code,),
        )
        station_codes = [i[0] for i in cursor.fetchall()]

        elements.append(
            svg.Image(
                href=href(f"../assets/codes/{station_code}.svg"),
                width=200,
                height=200,
                x=300 * i + 750,
                y=600
            )
        )

        elements.append(
            svg.ForeignObject(
                x=300 * i + 900,
                y=650,
                width=1000,
                height=100,
                text=html_station_name(
                    station_name, current_station, blur
                ),
                transform=f"rotate(-45 {300 * i + 650} 700)"
            ),
        )

        for j, code in enumerate(station_codes):
            elements.append(
                svg.Image(
                    href=href(f"../assets/codes/{code}.svg"),
                    width=200,
                    height=200,
                    x=300 * i + 750,
                    y=200 * j + 800,
                )
            )

        if i:
            arrow_length = 40 * 2 ** 0.5
            elements += [
                svg.Rect(
                    x=300 * i + 720 - arrow_length,
                    y=690,
                    width=arrow_length,
                    height=20,
                    fill=color,
                    rx=10,
                    ry=10,
                    transform=f"rotate(-45 {300 * i + 720} {700})"
                ),
                svg.Rect(
                    x=300 * i + 720 - arrow_length,
                    y=690,
                    width=arrow_length,
                    height=20,
                    fill=color,
                    rx=10,
                    ry=10,
                    transform=f"rotate(45 {300 * i + 720} {700})"
                )
            ]

        if blur:
            prev_blur = blurred(i-1, station_info, name, current_station)
            post_blur = blurred(i+1, station_info, name, current_station)
            if prev_blur and post_blur:
                fill = "#00000080"
            elif prev_blur and not post_blur:
                fill = "url(#outof_blur)"
            elif not prev_blur and post_blur:
                fill = "url(#into_blur)"
            else:
                fill = "url(#inandoutof_blur)"

            elements.append(
                svg.Rect(
                    x=300 * i + 675,
                    y=600,
                    width=300,
                    height=full_height - 1100,
                    fill=fill
                )
            )

    if "wise" in name and blurred(length-1, station_info, name, current_station):
        elements += [
            svg.Rect(
                x=300 * length + 675,
                y=600,
                width=300,
                height=full_height - 1100,
                fill="#00000080"
            ),
            svg.Rect(
                x=0,
                y=full_height - 500,
                width=full_width,
                height=200,
                fill="#00000080"
            ),
            svg.Rect(
                x=525,
                y=600,
                width=150,
                height=full_height - 1100,
                fill="url(#return_blur)"
            ),
        ]

    drawing = svg.SVG(
        width=full_width,
        height=full_height,
        elements=elements,
    )

    return drawing

def service_maps():
    cursor.execute("""
        SELECT Service.Name, Line.Name, Stations, Line.Color
        FROM Service INNER JOIN Line
        ON LineCode = Line.Code
    """)
    services = cursor.fetchall()
    for service in services:
        name, line, stations, color = service
        drawing = service_map(name, line, stations, color)        
        filename = f"../assets/service_maps/general/{line} {name}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(drawing))


def station_navigation():
    print("making station banners and navigation signs...")
    cursor.execute("""
        SELECT Name FROM Station
    """)
    stations = cursor.fetchall()

    subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/stations"])
    subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/navigation"])

    for i, row in enumerate(stations):
        station = row[0]
        print(f"making for {station}... ({i}/{len(stations)})")
        cursor.execute(
            """
            SELECT LineCode, Number 
            FROM StationCode INNER JOIN Line on LineCode = Line.Code
            WHERE StationName = ?
            ORDER BY CASE Type
                WHEN 'city'   THEN 1
                WHEN 'borough' THEN 2
                WHEN 'district'    THEN 3
                ELSE 4 -- Catches any other values
            END ASC
        """,
            (station,),
        )
        codes = cursor.fetchall()

        elements = [
            svg.Rect(x=0, y=0, width=2250, height=300, fill="black"),
            svg.Text(
                text=station,
                x=100,
                y=155,
                dominant_baseline="middle",
                font_size="110px",
                fill="white",
                font_family="Altone",
                font_weight=500,
            ),
        ]

        starting_x = 2250 - 50 - len(codes) * 225
        for i, (line, number) in enumerate(codes):
            elements.append(
                svg.Image(
                    href=href(f"../assets/codes/{line}{number}.svg"),
                    x=starting_x + i * 225,
                    y=50,
                    width=200,
                    height=200,
                )
            )

        station_drawing = svg.SVG(width=2250, height=300, elements=elements)

        filename = f"../assets/stations/{station}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(station_drawing))

        services = []
        raw_services = get_station_services(station, with_next=True)
        for platform in raw_services:
            services.append([])
            for raw_service in platform:
                if "wise" in raw_service[0]:
                    next_stations = [
                        i[1]
                        for i in surrounding_stations(
                            station, raw_service[1], raw_service[0]
                        )
                    ]
                else:
                    next_stations = [
                        end_destination(raw_service[1], raw_service[0])
                    ]
                for next_station in next_stations:
                    services[-1].append([*raw_service, next_station])

        if not services:
            continue

        if len(services) == 2:
            platform_directions = [[1], [], [], [2]]
        elif len(services) == 4:
            platform_directions = [[1], [2], [3], [4]]
        else:
            platform_directions = [[1], [2, 3], [5, 4], [6]]

        directions = [
            [service for i in d for service in services[i - 1]]
            for d in platform_directions
        ]

        top_rows = max(len(directions[0]), len(directions[3]))
        bottom_rows = max(len(directions[1]), len(directions[2]))

        height = (top_rows + bottom_rows) * 300 + 100

        elements = [
            svg.Rect(width=5000, height=height, x=0, y=0, fill="black"),
            # left arrow
            svg.Rect(
                width=37.5,
                height=125,
                x=75,
                y=75,
                fill="white",
                transform="rotate(45 75 200)",
            ),
            svg.Rect(
                width=37.5,
                height=125,
                x=75,
                y=200,
                fill="white",
                transform="rotate(-45 75 200)",
            ),
            svg.Rect(
                width=110,
                height=37.5,
                x=125,
                y=200 - 37.5 / 2,
                fill="white",
            ),
            # right arrow
            svg.Rect(
                width=37.5,
                height=125,
                x=4925,
                y=75,
                fill="white",
                transform="rotate(-135 4925 200)",
            ),
            svg.Rect(
                width=37.5,
                height=125,
                x=4925,
                y=200,
                fill="white",
                transform="rotate(135 4925 200)",
            ),
            svg.Rect(
                width=110,
                height=37.5,
                x=4765,
                y=200 - 37.5 / 2,
                fill="white",
            ),
            # left down arrow
            svg.Rect(
                width=37.5,
                height=150,
                x=75,
                y=top_rows * 300 + 125 - 37.5,
                fill="white",
                transform=f"rotate(45 {75 + 37.5 / 2} {top_rows * 300 + 275 - 37.5 / 2})",
            ),
            svg.Rect(
                width=37.5,
                height=150,
                x=75,
                y=top_rows * 300 + 125,
                fill="white",
                transform=f"rotate(90 {75 + 37.5 / 2} {top_rows * 300 + 275 - 37.5 / 2})",
            ),
            svg.Rect(
                width=37.5,
                height=150,
                x=75,
                y=top_rows * 300 + 125,
                fill="white",
            ),
            # right down arrow
            svg.Rect(
                width=37.5,
                height=150,
                x=4925 - 37.5,
                y=top_rows * 300 + 125 - 37.5,
                fill="white",
                transform=f"rotate(-45 {5000 - (75 + 37.5 / 2)} {top_rows * 300 + 275 - 37.5 / 2})",
            ),
            svg.Rect(
                width=37.5,
                height=150,
                x=4925 - 37.5,
                y=top_rows * 300 + 125,
                fill="white",
                transform=f"rotate(-90 {5000 - (75 + 37.5 / 2)} {top_rows * 300 + 275 - 37.5 / 2})",
            ),
            svg.Rect(
                width=37.5,
                height=150,
                x=4925 - 37.5,
                y=top_rows * 300 + 125,
                fill="white",
            ),
            # platforms
            svg.Image(
                href=href("../assets/platforms/1.svg"),
                width=200,
                height=200,
                x=300,
                y=100,
            ),
            svg.Image(
                href=href(
                    f"../assets/platforms/{platform_directions[3][0]}.svg"
                ),
                width=200,
                height=200,
                x=4500,
                y=100,
            ),
        ]

        # other platforms
        if platform_directions[1]:
            rows = 0
            for platform in platform_directions[1]:
                elements.append(
                    svg.Image(
                        href=href(f"../assets/platforms/{platform}.svg"),
                        width=200,
                        height=200,
                        x=300,
                        y=(top_rows + rows) * 300 + 100,
                    )
                )
                rows += len(services[platform - 1])

        if platform_directions[2]:
            rows = 0
            for platform in platform_directions[2]:
                elements.append(
                    svg.Image(
                        href=href(f"../assets/platforms/{platform}.svg"),
                        width=200,
                        height=200,
                        x=4500,
                        y=(top_rows + rows) * 300 + 100,
                    )
                )
                rows += len(services[platform - 1])

        # services
        offsets = [0, top_rows, top_rows, 0]
        for d in range(2):
            for i, (name, code, line, station_code) in enumerate(directions[d]):
                station_name = get_station_from_code(station_code)
                elements.append(
                    svg.Image(
                        href=href(f"../assets/lines/{line}.svg"),
                        width=200,
                        height=200,
                        x=575,
                        y=(offsets[d] + i) * 300 + 100,
                    )
                )
                # loop line
                if "wise" in name:
                    elements += [
                        svg.Text(
                            text=name,
                            x=850,
                            y=(offsets[d] + i) * 300 + 160,
                            dominant_baseline="middle",
                            font_size=125,
                            font_family="Altone",
                            font_weight=500,
                            fill="white",
                        ),
                        svg.ForeignObject(
                            x=850,
                            y=(offsets[d] + i) * 300 + 215,
                            width=1500,
                            height=100,
                            text=html_with_station(
                                "via", station=[station_name, station_code]
                            ),
                        ),
                    ]
                else:
                    length = 8 + len(name)
                    elements += [
                        svg.Text(
                            text=name,
                            x=850,
                            y=(offsets[d] + i) * 300 + 160,
                            dominant_baseline="middle",
                            font_size=125,
                            font_family="Altone",
                            font_weight=500,
                            fill="white",
                        ),
                        svg.ForeignObject(
                            x=850,
                            y=(offsets[d] + i) * 300 + 215,
                            width=1500,
                            height=100,
                            text=html_with_station(
                                "towards",
                                station=[station_name, station_code]
                                if station_name != station
                                else None,
                            ),
                        ),
                    ]

        for d in range(3, 1, -1):
            for i, (name, code, line, station_code) in enumerate(directions[d]):
                station_name = get_station_from_code(station_code)
                elements.append(
                    svg.Image(
                        href=href(f"../assets/lines/{line}.svg"),
                        width=200,
                        height=200,
                        x=4225,
                        y=(offsets[d] + i) * 300 + 100,
                    )
                )
                # loop line
                if "wise" in name:
                    length = 4 + len(name)
                    elements += [
                        svg.Text(
                            text=name,
                            x=4150,
                            y=(offsets[d] + i) * 300 + 160,
                            text_anchor="end",
                            dominant_baseline="middle",
                            font_size=125,
                            font_family="Altone",
                            font_weight=500,
                            fill="white",
                        ),
                        svg.ForeignObject(
                            x=2650,
                            y=(offsets[d] + i) * 300 + 215,
                            width=1500,
                            height=100,
                            text=html_with_station(
                                "via",
                                station=[station_name, station_code],
                                right=True,
                            ),
                        ),
                    ]
                else:
                    elements += [
                        svg.Text(
                            text=name,
                            x=4150,
                            y=(offsets[d] + i) * 300 + 160,
                            text_anchor="end",
                            dominant_baseline="middle",
                            font_size=125,
                            font_family="Altone",
                            font_weight=500,
                            fill="white",
                        ),
                        svg.ForeignObject(
                            x=2650,
                            y=(offsets[d] + i) * 300 + 215,
                            width=1500,
                            height=100,
                            text=html_with_station(
                                "towards",
                                station=[station_name, station_code]
                                if station_name != station
                                else None,
                                right=True,
                            ),
                        ),
                    ]

        navigation_drawing = svg.SVG(
            width=5000, height=height, elements=elements
        )

        filename = f"../assets/navigation/{station}.svg"
        subprocess.call(["/usr/bin/sudo", "touch", filename])
        subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
        with open(filename, "w") as f:
            f.write(str(navigation_drawing))

        subprocess.call(["mkdir", "-p", f"../assets/service_maps/{station}"])
        flat_services = [s for p in services for s in p]
        for name, line_code, line, _ in flat_services:
            cursor.execute("""
                SELECT Stations, Color
                FROM Service INNER JOIN Line
                ON LineCode = Line.Code
                WHERE Service.Name = ? AND LineCode = ?
            """, (name, line_code))
            service_stations, color = cursor.fetchone()
            drawing = service_map(name, line, service_stations, color, current_station=station)        
            filename = f"../assets/service_maps/{station}/{line} {name}.svg"
            subprocess.call(["/usr/bin/sudo", "touch", filename])
            subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
            with open(filename, "w") as f:
                f.write(str(drawing))


line_logos()
station_codes()
platform_logos()
service_maps()
station_navigation()
