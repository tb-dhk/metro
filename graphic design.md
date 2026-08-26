# representative codes, shapes and colors
each type of line has its own shape and code format.

| type     | shape   | code                                                      | hue                     | value and saturation                                                                    |
| -------- | ------- | --------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------- |
| city     | circle  | single letter                                             | from 12 standard colors | 100% saturation, lightness value that allows for a WCAG contrast score of 3.0 and above |
| borough  | diamond | single letter or number with optional alphanumeric suffix | ^                       | ^                                                                                       |
| district | square  | two letters                                               | standard grey           | <                                                                                       |
each line also has its own color and code, with borough lines sharing colors across the borough. see [[list of lines]] for more information.
## list of colors
### 12 standard colors
```palette
#804000 brown
#ff0000 red
#e87400 orange
#bd8e00 gold
#78a100 lime
#208000 green
#008075 turquoise
#009fd4 cyan
#0040ff blue
#000080 navy
#6000bf purple
#ff00ff pink
```
![[assets/lines/across bay line.svg|100]]![[assets/lines/sunset bay loop.svg|100]]![[assets/lines/island line.svg|100]]![[peninsula line.svg|100]]![[assets/lines/east coast line.svg|100]]![[assets/lines/airport express.svg|100]]![[pointer bay line.svg|100]]

## standard grey
```palette
grey: #808080
```
![[assets/lines/east ivy line.svg\|100]]![[assets/lines/central sheffield line.svg\|100]]![[assets/lines/east sheffield line.svg\|100]]![[assets/lines/fairview line.svg\|100]]![[assets/lines/holly heights line.svg\|100]]![[assets/lines/long island line.svg\|100]]![[assets/lines/west sheffield line.svg\|100]]![[assets/lines/boa island line.svg\|100]]![[assets/lines/pointer island line.svg\|100]]

# symbols
## font
all symbols use the altone font with medium or bold weight.
## line symbols
each line symbol is the representative shape of the line with the representative color of the line, and contains the line's code.

![[sunset bay loop.svg|100]]![[peninsula line.svg|100]]![[east sheffield line.svg|100]]

## station symbols
station codes look similar to line symbols and are of the same size, but they also contain a station number below the line code. 

![[B01.svg|100]]![[assets/codes/P01.svg|100]]![[assets/codes/ES01.svg|100]]

## platform logo
platform logos are white squares with black filling, also of size 200 px by 200 px. they have a 25 px wide white border and bold text of size 300.

![[1.svg|100]]
## full station logo
the full station logo contains the name of the station next to all of its station codes (one from each line).
![[elizabeth district.svg|1500]]
## navigation signs
the exact design of navigation signs varies a bit more, but these signs are mainly used at the exact center of the platform that is linked by escalators to the platforms. there are four possible directions: left, down and left, down and right, and right. navigation signs support up to two sides, where leftward directions appear on the left side and vice versa.

for each tier of lines a station serves, there will be one pair of platforms. higher-tier lines always use lower-numbered platforms. here is a comprehensive list of the platforms used by each tier in every possible scenario and the direction that the arrows will point in.

| city | borough | district | right | down and right | down and left | left |
| ---- | ------- | -------- | ----- | -------------- | ------------- | ---- |
| 1-2  | 3-4     | 5-6      | 1     | 2-3            | 4-5           | 6    |
| 1-2  | 3-4     | -        | 1     | 2              | 3             | 4    |
| 1-2  | -       | 3-4      | ^     | ^              | ^             | ^    |
| -    | 1-2     | 3-4      | ^     | ^              | ^             | ^    |
| 1-2  | -       | -        | 1     | -              | <             | 2    |
| -    | 1-2     | -        | ^     | ^              | ^             | ^    |
| -    | -       | 1-2      | ^     | ^              | ^             | ^    |

navigation signs contain a list of services, each assigned to a platform. they thus depict the direction the platform is in, the platform number and the services that use the platform. 

the arrows are on the very end (left or right) of the rows of the services corresponding to that direction. the platform numbers are next to the arrows, although more towards the middle. neither arrows nor platform numbers repeat, so they will only appear in the top row corresponding to them. the services on the same platforms and directions are thus expected to be grouped together.

for loops, each service name is either clockwise or anticlockwise, and the next station is indicated below the service name. for non-loops, the service name indicates the cardinal direction in which the service goes.
![[assets/navigation/elizabeth district.svg]]

the end destination is indicated below the service name, unless the service ends there, in which case the text below simply says "ends here".
![[assets/navigation/south coast.svg]]

for stations which are passed through more than once by the same service, the service will be repeated once for each pass, indicating the corresponding next station.
![[assets/navigation/robin cross.svg]]