# representative codes, shapes and colors
each type of line has its own shape and code format.

| type     | shape   | code          |
| -------- | ------- | ------------- |
| city     | circle  | letter        |
| borough  | diamond | letter/number |
| district | square  | two letters   |
each line also has its own color and code. see [[list of lines]] for more information.
# symbols
## text
all symbols use the altone font. text is aligned based on the text anchor point.
## line symbols
each line symbol is the representative shape of the line with the representative color of the line, with size 200 px by 200 px. the line's code is in the middle of the symbol. it is bold and white, with size 100.
![[sunset bay loop.svg]]![[island line.svg]]![[east sheffield line.svg]]

## station symbols
station codes look similar to line symbols and are of the same size, but they also contain a station number below the line code. both are bold and white, but the line code has size 90 and the station number has size 60. the line code and station number are spaced evenly with the top and bottom, except for the diamond (used for borough lines) where they are spaced evenly with the top and the line $y=175$.

![[B01.svg|200]]![[assets/codes/I01.svg]]![[assets/codes/ES01.svg|200]]

## platform logo
platform logos are white squares with black filling, also of size 200 px by 200 px. they have a 25 px wide white border and bold text of size 300.
![[1.svg]]
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

each row, containing one service on each side, is 300 px tall. line and platform logos are of size 200 px by 200 px, and text also keeps within the 200 px height, leaving a 50 px margin on the top and bottom of each row.

arrows are of width 150, made up of three rectangles where the two ends forming the arrow head are perpendicular to each other and the stem of the arrow is at a $45\degree$ angle to both. each arrow fits snugly in a square.

the horizontal spacing between elements (arrows, platform logos, line logos and descriptive text) is 75 px each.

for lines, the main text size is 350 and indicates the end destination. the station code of the end destination is 50 px to its right with size 150 px by 150 px, aligned vertically with the middle of the row. the text box is 101.1 px from the top of the row.

for loops, the main text size is 350 and indicates the direction (clockwise or anticlockwise). the top of the main text is aligned with the top of the row (below the margin). below, smaller text of size 175 indicates the next major station in the line that the train will be passing through. the station code is 25 px to its right with size 100 px by 100 px, and is aligned vertically with the smaller text.

![[assets/navigation/elizabeth district.svg]]