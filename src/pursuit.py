#!/usr/bin/env python

# File name: pursuit.py
# Author: Sean Carter
# Python Version: 2.7

from getAngle import getSamples, sampleToAngle #Our functions to deal with sound correlation
import math
import os
import subprocess
import rospy
from threading import Thread
from geometry_msgs.msg import Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry

def make_marker(angle):
	""" Creates Marker for a sphere at a specified location

		Args:
			angle: angle from

		Returns:
			A Marker, pointed in the direction the robot
			thinks it has heard sound from."""
	my_marker = Marker(type=Marker.ARROW)
	my_marker.header.frame_id = "odom"

	#We only rotate in one plaen, quaternion only uses two values
	quaternion = quaternion_from_euler(math.radians(angle),0.0,0.0)
	my_marker.pose.orientation.x = quaternion[0]
	my_marker.pose.orientation.w = quaternion[3]

	#Setting the size of the arrow
	my_marker.scale.x = .5
	my_marker.scale.y = .1
	my_marker.scale.z = .1
	return my_marker

def constant_record_and_copy(callback):
	while True:
		print "Recording new file."
		#These lines record the audio, and copy it onto our computer
		subprocess.call('ssh pi@192.168.17.201 /home/pi/use_case_scripts/ride-of-the-neatos/Record_from_lineIn_Micbias_modified.sh > /dev/null', shell=True)
		subprocess.call('scp pi@192.168.17.201:/home/pi/wavFile.wav ~/catkin_ws/src/ride-of-the-neatos/src', shell=True)
		callback()
		# err = os.system("ssh pi@192.168.17.201 /home/pi/use_case_scripts/ride_of_the_neatos/Record_from_lineIn_Micbias.sh > /dev/null")
		# if err != 0:
		# 	print "Error recording on Pi"
		#
		# err = os.system("scp pi@192.168.17.201:/home/pi/wavFile.wav ~/catkin_ws/src/ride-of-the-neatos/src")
		# if err != 0:
		# 	print "Error copying file from Pi"

def get_distance(angle1, angle2):
    phi = abs(angle2-angle1) % 2*math.pi
    sign = 1
    # used to calculate sign
    if not ((angle1-angle2 >= 0 and angle1-angle2 <= math.pi) or (
            angle1-angle2 <= -math.pi and angle1-angle2 >= -2*math.pi)):
        sign = -1
    if phi > math.pi:
        result = math.pi-phi
    else:
        result = phi

    return result*sign


class audioFollower(object):
	""" Creates a ros node to command a neato to follow an audio source"""
	def __init__(self):
		rospy.init_node("audioFollower")
		rospy.Subscriber("/odom", Odometry, self.process_position)
		self.commander = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		self.arrow = rospy.Publisher("/audio_src", Marker, queue_size=10)
		self.target_angle = None
		self.theta = None
		self.r = rospy.Rate(10)


	def createVelocity(self):
		""" Creates proportional controller to center on last
			recieved location of audio source: the further it is
			from an area in front of the robot, the faster
			it tries to center it

			Returns:
				Twist message: telling the neato how fast to turn,
				and how fast to move forwards (not fast).
		"""
		spin = Twist()
		distance = get_distance(self.target_angle, self.theta)
		spin.angular.z = 0.3*distance
		spin.linear.x = .1
		return spin

	def updateTargetAngle(self):
		#Use functions created to identify audio angle
		samps = getSamples("wavFile.wav")
		print "Getting audio"
		ang = - sampleToAngle(samps)
		print ang
		self.target_angle = self.theta + math.radians(ang)
		self.publishAngle()

	def process_position(self, m):
		""" Get theta from pose (geometry_msgs.Pose)"""
		pose = m.pose.pose
		orientation_tuple = (pose.orientation.x,
							 pose.orientation.y,
							 pose.orientation.z,
							 pose.orientation.w)
		angles = euler_from_quaternion(orientation_tuple)
		self.theta = angles[2]

	def publishAngle(self):
		arrow_marker = make_marker(self.target_angle)
		self.arrow.publish(arrow_marker)

	def run(self):
		thread = Thread(target = constant_record_and_copy, args = (self.updateTargetAngle, ))
		thread.start()
		while self.target_angle == None or self.theta == None:
			self.r.sleep()
		while not rospy.is_shutdown():
			self.commander.publish(self.createVelocity())
			#print "Angling."
			print self.target_angle
			print self.theta
			self.r.sleep()

if __name__ == '__main__':
	node = audioFollower()
	node.run()
