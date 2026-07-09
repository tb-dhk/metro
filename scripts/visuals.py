import svg
import sqlite3
import subprocess
import base64
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
                transform=f"rotate(45, 100, 100)",
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
                y=110,
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

print("making station banners and navigation signs...")
cursor.execute("""
    SELECT Name FROM Station
""")
stations = cursor.fetchall()

subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/stations"])
subprocess.call(["/usr/bin/sudo", "mkdir", "../assets/navigation"])

for row in stations:
    station = row[0]
    cursor.execute(
        """
        SELECT LineCode, Number FROM StationCode
        WHERE StationName = ?
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
            if raw_service[0][-4:] == "wise":
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
        svg.Rect(width=4000, height=height, x=0, y=0, fill="black"),
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
            x=3925,
            y=75,
            fill="white",
            transform="rotate(-135 3925 200)",
        ),
        svg.Rect(
            width=37.5,
            height=125,
            x=3925,
            y=200,
            fill="white",
            transform="rotate(135 3925 200)",
        ),
        svg.Rect(
            width=110,
            height=37.5,
            x=3765,
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
            x=3925 - 37.5,
            y=top_rows * 300 + 125 - 37.5,
            fill="white",
            transform=f"rotate(-45 {4000 - (75 + 37.5 / 2)} {top_rows * 300 + 275 - 37.5 / 2})",
        ),
        svg.Rect(
            width=37.5,
            height=150,
            x=3925 - 37.5,
            y=top_rows * 300 + 125,
            fill="white",
            transform=f"rotate(-90 {4000 - (75 + 37.5 / 2)} {top_rows * 300 + 275 - 37.5 / 2})",
        ),
        svg.Rect(
            width=37.5,
            height=150,
            x=3925 - 37.5,
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
            href=href(f"../assets/platforms/{platform_directions[3][0]}.svg"),
            width=200,
            height=200,
            x=3500,
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
                    x=3500,
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
            if name[-4:] == "wise":
                elements += [
                    svg.Text(
                        text=name,
                        x=850,
                        y=(offsets[d] + i) * 300 + 165,
                        dominant_baseline="middle",
                        font_size=125,
                        font_family="Altone",
                        font_weight=500,
                        fill="white",
                    ),
                    svg.ForeignObject(
                        x=850,
                        y=(offsets[d] + i) * 300 + 220,
                        width=1000,
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
                        y=(offsets[d] + i) * 300 + 165,
                        dominant_baseline="middle",
                        font_size=125,
                        font_family="Altone",
                        font_weight=500,
                        fill="white",
                    ),
                    svg.ForeignObject(
                        x=850,
                        y=(offsets[d] + i) * 300 + 220,
                        width=1000,
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
                    x=3225,
                    y=(offsets[d] + i) * 300 + 100,
                )
            )
            # loop line
            if name[-4:] == "wise":
                length = 4 + len(name)
                elements += [
                    svg.Text(
                        text=name,
                        x=3150,
                        y=(offsets[d] + i) * 300 + 165,
                        text_anchor="end",
                        dominant_baseline="middle",
                        font_size=125,
                        font_family="Altone",
                        font_weight=500,
                        fill="white",
                    ),
                    svg.ForeignObject(
                        x=2150,
                        y=(offsets[d] + i) * 300 + 220,
                        width=1000,
                        height=100,
                        text=html_with_station(
                            "via",
                            station=[station_name, station_code],
                            right=True,
                        ),
                    ),
                ]
            else:
                length = 8 + len(name)
                elements += [
                    svg.Text(
                        text=name,
                        x=3150,
                        y=(offsets[d] + i) * 300 + 165,
                        text_anchor="end",
                        dominant_baseline="middle",
                        font_size=125,
                        font_family="Altone",
                        font_weight=500,
                        fill="white",
                    ),
                    svg.ForeignObject(
                        x=2150,
                        y=(offsets[d] + i) * 300 + 220,
                        width=1000,
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

    navigation_drawing = svg.SVG(width=4000, height=height, elements=elements)

    filename = f"../assets/navigation/{station}.svg"
    subprocess.call(["/usr/bin/sudo", "touch", filename])
    subprocess.call(["/usr/bin/sudo", "chmod", "777", filename])
    with open(filename, "w") as f:
        f.write(str(navigation_drawing))
