import cv2
import cv2.aruco as aruco
import matrix
import Filter
import pickle
import numpy as np

class ArucoDetector:

	def __init__(self):
		self.markerLength = 0.1		
		self.ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_1000)
		self.cameraMatrix = None
		self.distCoeffs = None
		self.parameters = aruco.DetectorParameters_create()
		self.parameters.cornerRefinementMinAccuracy = 1e-20
		self.parameters.cornerRefinementMaxIterations = 100
		self.parameters.cornerRefinementWinSize = 10
		self.parameters.cornerRefinementMethod = aruco.CORNER_REFINE_APRILTAG
		self.parameters.errorCorrectionRate = 0
		self.tfs = [None]*1000

	def LoadCalibration(self,fileName):
		try:
			f = open(fileName, 'rb')
			(self.cameraMatrix, self.distCoeffs) = pickle.load(f)
			f.close()
			return True
		except:
			print('Cant load calibration file: ' + filename)
			return False

	def Settings(self,aruco_dict,markerLength,ids,tfMatrixs, cornerRefinementMethod=aruco.CORNER_REFINE_APRILTAG):
		self.ARUCO_DICT = aruco_dict
		self.markerLength = markerLength
		self.parameters.cornerRefinementMethod = cornerRefinementMethod
		self.__Set3DGridboard(ids,tfMatrixs)

	def DetectPoseOf3DGridboard(self,QueryImg):
		if (self.__IsCalibrated()):
			corners, ids, rejectedImgPoints = self.__DetectMarkers(QueryImg)
			if ids is not None:
				rvecs, tvecs = self.__EstimatePoseSingleMarkers(corners)
				tvecsEff = []
				rvecsEff = []
				arrayEuler = []
				arrayTvec = []
				index = 0
				for idTag in ids:
					if self.tfs[idTag[0]] is not None:
						mat = cv2.Rodrigues(rvecs[index])
						euler = matrix.rotationMatrixToEulerAngles(mat[0])
						rE,tE, _ = self.__GetParam(idTag,tvecs,mat,index)
						tvecsEff.append(tE)
						rvecsEff.append(rE)
					index += 1
				if len(tvecsEff)>0: 
					arrayTvec,arrayEuler, content = Filter.PoseEstimate(tvecsEff,rvecsEff)
				if(len(arrayTvec) > 0):
					matRvec = matrix.eulerAnglesToRotationMatrix(arrayEuler)
					effRvec = cv2.Rodrigues(matRvec)
					aruco.drawAxis(QueryImg,self.cameraMatrix,self.distCoeffs,effRvec[0],arrayTvec,0.1)
					return True,QueryImg,arrayTvec,arrayEuler, content
			return False,QueryImg,None,None,None

		else:
			print('Need calibration File!')
			return False,QueryImg,None,None,None


	# -------------------------------------------- PRIVATE ------------------------------------------- #

	def __CreateGrayImage(self,QueryImg):
		return cv2.cvtColor(QueryImg, cv2.COLOR_BGR2GRAY)

	def __IsCalibrated(self):
		if(self.cameraMatrix is not None and self.distCoeffs is not None):
			return True
		else:
			return False

	def __Set3DGridboard(self,ids,tfsMat):
		if(len(ids) == len(tfsMat)):
			index = 0
			for idTag in ids:
				self.tfs[idTag] =  tfsMat[index]
				index += 1
		else:
			print('3D gridboard definition fail')

	def __DetectMarkers(self,QueryImg):
		gray = self.__CreateGrayImage(QueryImg)
		corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.ARUCO_DICT, parameters=self.parameters)
		return corners, ids, rejectedImgPoints
	
	def __EstimatePoseSingleMarkers(self,corners):

		rvecs, tvecs,_ =  aruco.estimatePoseSingleMarkers(corners, self.markerLength, self.cameraMatrix, self.distCoeffs)
		return rvecs, tvecs
		
	def __GetParam(self,idTag,tvecs,mat,i):
		m = self.tfs[idTag[0]]
		invMat = matrix.InversMatrix(m)
		Mat4x4 = matrix.Create4x4Mat(mat[0],tvecs[i][0])
		posOfEff = Mat4x4 * invMat   
		rE = matrix.rotationMatrixToEulerAngles(posOfEff)
		tE = np.array([posOfEff[0][0,3],posOfEff[1,3],posOfEff[2,3]])
		return rE,tE, idTag[0]































