#!/usr/bin/env python
# # license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray

class Ros_talkers:
   encoder_feedback = pyqtSignal()
   
   def talker():
      pub = rospy.Publisher('chatter', String, queue_size=10)
      rospy.init_node('talker', anonymous=True)
      rate = rospy.Rate(10) # 10hz
      while not rospy.is_shutdown():
         hello_str = "hello world %s" % rospy.get_time()
         rospy.loginfo(hello_str)
         pub.publish(hello_str)
         rate.sleep()

   def callback(data):
      rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
      self.encoder_feedback.emit(data)
      


   def listener():
      rospy.init_node('joint_feeback_listener', anonymous=True)
    
      rospy.Subscriber("joint_feedback", Float32MultiArray, callback)
      rospy.spin()