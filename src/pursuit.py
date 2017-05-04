#!/usr/bin/env python

# File name: pursuit.py
# Author: Sean Carter
# Python Version: 2.7

import getAngle #Our functions to deal with sound correlation
import math
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker

def make_marker(angle):
	""" Creates Marker for a sphere at a specified location

		Args:
			angle: angle from

		Returns:
			A Marker, pointed in the direction the robot
			thinks it has heard sound from."""
	my_marker = Marker(type=Marker.ARROW)
	my_marker.header.frame_id = "base_link"

	#We only rotate in one plaen, quaternion only uses two values
	quaternion = quaternion_from_euler(math.radians(angle))
	my_marker.pose.orientation.x = quaternion[0]
	my_marker.pose.orientation.w = quaternion[3]

	#Setting the size of the arrow
	my_marker.scale.x = .5
	my_marker.scale.y = .1
	my_marker.scale.z = .1
	return my_marker

class audioFollower(object):
	""" Creates a ros node to command a neato to follow an audio source"""
	def __init__(self):
		rospy.init_node("audioFollower")
		self.r = rospy.Rate(5)
		self.commander = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		self.arrow = rospy.Publisher("/direction", Marker, queue_size=10)
		self.angle = None

		#Waits for first measurement to start following the audio
		while self.angle == None:
			self.r.sleep()

    def createVelocity(self):
		""" Creates proportional controller to follow audio source:
			the further is is from an area in front of the
			robot, the faster it tries to center it

			Returns:
				Twist message: telling the neato how fast to turn,
				and how fast to move forwards (not fast).
		"""
		spin = Twist()
		spin.angular.z = .9*(self.angle/90.0)
		spin.linear.x = .2
		return spin

	def findAudioAngle(self):
		#These lines record the audio, and copy it onto our computer
		os.system("ssh pi@192.168.17.201 /home/pi/use_case_scripts/ride_of_the_neatos/Record_from_lineIn_Micbias.sh")
        os.system("scp pi@192.168.17.201:~/use_case_scripts/ride_of_the_neatos/wavFile.wav ~/catkin_ws/src/ride_of_the_neatos/src")

		#Use functions created to identify audio angle
		samps = getSamples("wavFile.wav")
	    ang = sampleToAngle(samps)
		self.angle = ang

	def publishAngle(self):
		arrow_marker = make_marker(self.angle)
		self.arrow.publish(arrow_marker)

    def run(self):
		while not rospy.is_shutdown():
			self.findAudioAngle()
			self.publishAngle()
			self.commander.publish(self.createVelocity())
			self.r.sleep()

if __name__ == '__main__':
	node = audioFollower()
	node.run()
