# #
# # This is a demo program showing CameraServer usage with OpenCV to do image
# # processing. The image is acquired from the USB camera, then a rectangle
# # is put on the image and sent to the dashboard. OpenCV has many methods
# # for different types of processing.
# #
# # NOTE: This code runs in its own process, so we cannot access the robot here,
# #       nor can we create/use/see wpilib objects
# #
# # To try this code out locally (if you have robotpy-cscore installed), you
# # can execute `python3 -m cscore vision.py:main`
#
#
#
# # https://docs.wpilib.org/en/stable/docs/software/vision-processing/roborio/using-multiple-cameras.html
# # https://github.com/robotpy/robotpy-cscore/blob/main/examples/dual_cameraserver.py
#
# import cv2
# import numpy as np
#
# # from cscore import CameraServer
#
#
# def main():
#     cs = CameraServer.getInstance()
#     cs.enableLogging()
#
#     # camera = cs.startAutomaticCapture()
#     cam1 = cs.startAutomaticCapture(dev=0)
#     # cam2 = cs.startAutomaticCapture(dev=1)
#
#     cs.waitForever()
#
# if __name__ == "__main__":
#
#     # To see messages from networktables, you must setup logging
#     import logging
#
#     logging.basicConfig(level=logging.DEBUG)
#
#     # You should uncomment these to connect to the RoboRIO
#     import networktables
#     networktables.initialize(server='10.41.69.2')
#
#     main()
