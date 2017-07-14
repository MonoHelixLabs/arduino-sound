"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""

"""
This code is based on the script provided by electronut.in, as shown above.

It has been modified to read 5 sensor values, add a legend with the name of 
some toys and their color, and to capture a picture when the "save" 
string is sent on the serial port (sent when a button is pressed on the 
Arduino).

"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
import datetime

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.a0 = deque([0.0]*maxLen)
      self.a1 = deque([0.0]*maxLen)
      self.a2 = deque([0.0]*maxLen)
      self.a3 = deque([0.0]*maxLen)
      self.a4 = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == 5)
      self.addToBuf(self.a0, data[0])
      self.addToBuf(self.a1, data[1])
      self.addToBuf(self.a2, data[2])
      self.addToBuf(self.a3, data[3])
      self.addToBuf(self.a4, data[4])

  # update plot
  def update(self, frameNum, a0, a1, a2, a3, a4):
      try:
          line = self.ser.readline()
          if line.startswith(b'save'):
              plt.savefig('test_'+'{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now())+".png")
              return None
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 5):
              self.add(data)
              a0.set_data(range(self.maxLen), self.a0)
              a1.set_data(range(self.maxLen), self.a1)
              a2.set_data(range(self.maxLen), self.a2)
              a3.set_data(range(self.maxLen), self.a3)
              a4.set_data(range(self.maxLen), self.a4)
      except KeyboardInterrupt:
          print('exiting')
      
      return a0,

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 200)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 200), ylim=(0, 4))
  ax0, = ax.plot([], [], label="tortoise", color="green")
  ax1, = ax.plot([], [], label="koala", color="grey")
  ax2, = ax.plot([], [], label="dolphin", color="blue")
  ax3, = ax.plot([], [], label="giraffe", color="orange")
  ax4, = ax.plot([], [], label="crocodile", color="black")
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(ax0, ax1, ax2, ax3, ax4), 
                                 interval=4)

  plt.legend(handles=[ax0,ax1,ax2,ax3,ax4])
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()