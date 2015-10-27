#!/usr/bin/env python
import rospy
from joint_estimation.msg import AxesValues
from Adafruit_I2C import Adafruit_I2C

# Mag 3310 Driver Class
class Mag_Driver():

  def __init__(self):
    # Get the ~private namespace parameters from command line or launch file
    rate = float(rospy.get_param('~rate', '10.0'))
    address = rospy.get_param('~address', '0x60')
    

    # Create message object
    address = 0x60
    DEVICE_REG = 1
    i2c = Adafruit_I2C(address)

    # Create a publisher for magnet messages
    pub = rospy.Publisher("magnet_topic", AxesValues)
    msg = AxesValues()
    msg.x_axis = 0
    msg.y_axis = 0
    msg.z_axis = 0

    print "Initialize"

    # Main while loop
    while not rospy.is_shutdown():
      print "Main loop"
      i2c.write8(DEVICE_REG, 0x01) #FIXME is this needed?

      # read in six bytes of message
      data = []
      # Make list of 6 bytes
      for i in range (0, 6):
        data.append(i2c.readU8(DEVICE_REG))

      msg.x_axis = (data[0] << 8) + data[1]
      msg.y_axis = (data[2] << 8) + data[3]
      msg.z_axis = (data[4] << 8) + data[5]
      
      # publish data out
      pub.publish(msg)
     
      # Sleep for a while before publishing new messages
      if rate:
        rospy.sleep(1/rate)
      else:
        rospy.sleep(1.0)

# Main function
if __name__ == '__main__':
  rospy.init_node('mag3110_driver')
  print "calling main"
  # Go to class functions that do all the heavy lifting. Do error checking.
  md = Mag_Driver()  
  try:
    md = Mag_Driver()  
  except rospy.ROSInterruptException: pass