# Ride of the Neatos
###### Final project for CompRobo2017
###### By Jeff, Marissa, and Sean

### What is this project?
Ride of the neatos is a project designed to allow a robotic vacuum cleaner to follow a sound source. We used "Ride of the Valkyries" for most of our tests. 

### How to use:
This code requires Scipy and Ros. Ros can be installed using the installation instructions [here](http://wiki.ros.org/kinetic/Installation). On Ubuntu, Scipy can be installed with ```sudo pip install scipy```.

The code for the neatos is in Paul Ruvolo's [CompRobo](https://github.com/paulruvolo/comprobo17) repository. Both that code, and this repository, should be located in the /src director inside your catkin workspace.

You must also have a Raspberry Pi, with a Cirrus Logic sound card and stereo microphones. For the card to work correctly, you should follow the installation instructions [here](https://www.element14.com/community/thread/42202/l/cirrus-logic-audio-card-working-on-the-raspberry-pi-2?displayFullThread=true). Finally, you will need to have paswordless ssh set up to communicate with this pi. Instructions to set this up are located at [linuxproblem.org](http://www.linuxproblem.org/art_9.html).

Once these are installed, you can launch the program by running roscore, launching the neato program in the CompRobo directory, and running ```pursit.py``` from this repository.
