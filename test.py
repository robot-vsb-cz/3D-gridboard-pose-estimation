from Aruco import ArucoDetector as aruco
import numpy as np
import cv2.aruco as aru
import pyrealsense2 as rs
import time
import cv2


ar = aruco()
ar.LoadCalibration('calibrationD435iPython2.pckl')



m0=np.array(	[[1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
 		[0.00000000e+00, 1.00000000e+00, 0.00000000e+00, 0.00000000e+00],
		[0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00],
 		[0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

m1=np.array(	[[ 0.96592581,  0.0,         -0.25881911, -0.1       ],
		[ 0.0,          1.0,          0.          ,0.0        ],
		[ 0.25881911,  0.0,          0.96592581, -0.012941  ],
		[ 0.0,          0.0,          0.0,          1.0        ]])

m2=np.array(	[[-4.37113900e-08,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00],
		[-9.65925817e-01, -4.22219601e-08, -2.58819081e-01,  -1.00000001e-01], # -1.00000001e-01
		[-2.58819081e-01, -1.13133418e-08,  9.65925817e-01,  -1.29410001e-02],
		[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])

m3=np.array(	[[-9.65925809e-01, -8.44439195e-08,  2.58819110e-01,  1.00000001e-01],
		[ 8.74227800e-08, -1.00000000e+00,  0.00000000e+00,  0.00000000e+00],
		[ 2.58819110e-01,  2.26266861e-08,  9.65925809e-01, -1.29410001e-02],
		[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])

m4=np.array(	[[-4.37113900e-08, -1.00000000e+00,  0.00000000e+00,  0.00000000e+00],
		[ 9.65925824e-01, -4.22219604e-08,  2.58819052e-01,  1.00000001e-01],
		[-2.58819052e-01,  1.13133405e-08,  9.65925824e-01, -1.29410001e-02],
		[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])

effector = np.array([m0,m1,m2,m3,m4])
ids = np.array([0,1,2,3,4])
aruco_dict = aru.Dictionary_get(aru.DICT_6X6_1000)
ar. Settings(aruco_dict,0.07,ids,effector)

# for RealSense Cameras 
ctx = rs.context()
idCam = ctx.devices[0].get_info(rs.camera_info.serial_number)
pipeline = rs.pipeline()
config = rs.config()
config.enable_device(idCam)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8,30)
pipeline.start(config)



def GetImageFromRS():
	global pipeline 
	frames = pipeline.wait_for_frames()
	colr = frames.get_color_frame()
	#colr = frames.first(rs.stream.infrared)
	colr = frames.get_color_frame()
	color_image = np.asanyarray(colr.get_data())
	return color_image


try:
	while(True):
		if True:
			img = GetImageFromRS()
			ifdetect ,image,_,_,_ = ar.DetectPoseOf3DGridboard(img)
			cv2.imshow('Image', image)
			ch = cv2.waitKey(1)
except KeyboardInterrupt:
	exit()