Summary of task

The objective of the task was to create a Python script that would produce various types of lego
pieces. The pieces needed to have accurate dimensions according to the official lego pieces. To
achieve this task a GUI must be built which one would interact with to create the lego pieces.
The GUI should be easy to use.
Once the script is written, the GUI must be used to create pieces to build an accurate
representation of a lego tech vehicle. The vehicle should be rendered as an image that would
look like a lego box cover.

Method and Approach

The General approach was first to go through the tutorial to learn about pythons syntax and
creating lego pieces. Once I had completed the tutorial I restructured the GUI so that it made
sense according to the assignment. One chooses the color once which sets it for all the pieces.
To change the color they have to reselect the color. The basic block has a width and length. The
beams have a length chosen by slider. The angled beam you can also select between the angles
of 90 and 45. These were the only angles I needed to create my model. To create the wheel and
hub, you only push a button and it is instantly created.
Once the GUI was set up I made the main functions the buttons would call. Each one of these
functions’ uses subfunctions to create the designated object. For example each function calls
the addcolor function at the end of it.
The basic block was given to us in the tutorial so I started with that. I took the basic block and
added more cylinders which use a Boolean difference to create the holes in the blocks. As well I
made it so it puts pipes on top of the block instead of solid cylinders.
I removed the name spacing because it caused more hassle then it was worth. Instead I set a
global variable of the name of the object. Each time a Boolean is done it resets it to the global
variable.
With the basic block and beam done I moved to the round beams. I created the round edges by
moving the cylinders to the edge of the square on either side and Boolean joined them. I then
reused the holes and extrusion functions.
To create the angle I created two round beams. The second is half the width of the first. I then
moved the rotation orientation to the bottom of the second round beam, rotated and shifted it
to it matched up with the first beam.
I created the wheels by extruding selected faces and adding cylinders in the middle.
To create the axels I used Booleans and shifted around cylinders for these Booleans. Each axel
uses the base axel function then adds onto it.
To create the maya model I created the pieces using my GUI . I used online instructions step by
step to create my vehicle. There were many steps. Some parts such as the physical motor for
the car I did not include because I ran out of extra shapes I could make.