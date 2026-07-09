# locations
## `Borough` table

| name   | type | notes                        |
| ------ | ---- | ---------------------------- |
| `Code` | text | primary key, 1-5, "P" or "I" |
| `Name` | text |                              |
## `District` table

| name      | type | notes                          |
| --------- | ---- | ------------------------------ |
| `Code`    | text | primary key, two letters       |
| `Name`    | text |                                |
| `Borough` | text | foreign key for `Borough.Code` |

## `Station` table
each station directly corresponds to one neighborhood.

| name        | type    | notes                           |
| ----------- | ------- | ------------------------------- |
| `Name`      | text    | primary key                     |
| `District`  | text    | foreign key for `District.Code` |
| `Operating` | integer | boolean                         |

# lines
## `Line` table

| name    | type | notes                                          |
| ------- | ---- | ---------------------------------------------- |
| `Code`  | text | primary key, up to two alphanumeric characters |
| `Name`  | text | primary key                                    |
| `Type`  | text | "city", "borough" or "district"                |
| `Area`  | text | borough or district name                       |
| `Color` | text | hex code starting with \#                      |
## `Service` table

| name       | type    | notes                                                                                                                                                     |
| ---------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Name`     | text    | primary key                                                                                                                                               |
| `Line`     | text    | primary key, foreign key for `Line.Code`                                                                                                                  |
| `Stations` | text    | string containing station codes, comma-separated. may use `A...B` to indicate passing through all consecutive stations from `A` to `B` in numerical order |
| `Platform` | integer | 1 or 2, indicator of odd or even platform                                                                                                                 |

## `StationCode` table
| name      | type | notes                                                  |
| --------- | ---- | ------------------------------------------------------ |
| `Line`    | text | primary key, foreign key for `Line.Code`               |
| `Number`  | text | primary key, two-digit number (leading zero if needed) |
| `Station` | text | foreign key for `Station.Name`                         |
