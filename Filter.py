import math
import numpy as np



def PoseEstimate(tvecs,rvec):
	x = []
	y = []
	z = []
	distances = []
	estimatedX = 0
	estimatedY = 0
	estimatedZ = 0


	for i in range(0,len(tvecs)):
		dist = 0
		for j in range(0,len(tvecs)):
			dist += GetDistance(tvecs[i],tvecs[j])
	
		distances.append(dist)
		x.append(GetNumFromArray(tvecs[i],'x'))
		y.append(GetNumFromArray(tvecs[i],'y'))
		z.append(GetNumFromArray(tvecs[i],'z'))

	maximum = max(distances)
	index = FindIndexOfMaximum(distances,maximum)
	if len(tvecs)>2:
		xFiltred = []
		yFiltred = []
		zFiltred = []
		for k in range(0,len(x)):
			if k != index:
				estimatedX += x[k]
				estimatedY += y[k]
				estimatedZ += z[k]
				xFiltred.append(x[k])
				yFiltred.append(y[k])
				zFiltred.append(z[k])

		lenOfEstimateArray = len(x) - 1 		
		estimatedX /=  lenOfEstimateArray
		estimatedY /=  lenOfEstimateArray
		estimatedZ /=  lenOfEstimateArray
				
		content = Content(xFiltred,yFiltred,zFiltred)
		rvecs = AngleEstimate(rvec,index)
		return np.array([estimatedX,estimatedY,estimatedZ]),rvecs, content
	else:
		lenOfEstimateArray = len(tvecs)
		for i in range(0,lenOfEstimateArray):
			estimatedX += GetNumFromArray(tvecs[i],'x')
			estimatedY += GetNumFromArray(tvecs[i],'y')
			estimatedZ += GetNumFromArray(tvecs[i],'z')
		estimatedX /=  lenOfEstimateArray
		estimatedY /=  lenOfEstimateArray
		estimatedZ /=  lenOfEstimateArray
		rvecs = AngleEstimate(rvec,index)
	
		return np.array([estimatedX,estimatedY,estimatedZ]),rvecs, 0	


# the volume of the cube (max detected range) aligned with the coordinate system
def Content(arrayX,arrayY,arrayZ):
	maxX = max(arrayX)
	maxY = max(arrayY)
	maxZ = max(arrayZ)

	minX = min(arrayX)
	minY = min(arrayY)
	minZ = min(arrayZ)

	X = maxX - minX
	Y = maxY - minY
	Z = maxZ - minZ
	return X*Y*Z*1000000 

def FindIndexOfMaximum(array,maximum):
	index = 0	
	for dist in array:
		if dist == maximum:
			break
		index += 1
	return index

# for clarity
def GetNumFromArray(array,arg):
	num = 0
	if arg == 'x':
		num = array[0]
	if arg == 'y':
		num = array[1]
	if arg == 'z':
		num = array[2]
	return num

def GetDistance(pointA,pointB):
	x = abs(GetNumFromArray(pointA,'x') - GetNumFromArray(pointB,'x'))
	y = abs(GetNumFromArray(pointA,'y') - GetNumFromArray(pointB,'y'))
	z = abs(GetNumFromArray(pointA,'z') - GetNumFromArray(pointB,'z'))
	dist = math.sqrt(pow(x,2)+pow(y,2)+pow(z,2))
	return dist

def AngleEstimate(rvecs,index):
	alfaArray = []
	betaArray = []
	gamaArray = []
	for angles in rvecs:
		alfaArray.append(angles[0])
		betaArray.append(angles[1])
		gamaArray.append(angles[2])
	alfa = AlfaEstimate(alfaArray,index)
	beta = SortAngleArray(betaArray,index)
	gama = SortAngleArray(gamaArray,index)
	
	array =np.array([alfa,beta,gama])	
	return array	
		

def AlfaEstimate(alfaArray,_index):
	index  = 0
	for alfa in alfaArray:
		if alfa < 0:
			alfaArray[index] = alfa + 2 * math.pi
		index += 1
	alfa = 	SortAngleArray(alfaArray,_index)	
	return alfa

def GamaEstimate(gamaArray):
	index  = 0
	for gama in gamaArray:
		if gama > 3.14:
			gamaArray[index] = -gama+math.pi
		index += 1

	gama = 	SortAngleArray(gamaArray)	
		
	return gama

def SortAngleArray(array,index):
	array = FindJump(array)
	if(len(array)>2):
		distances = []
		dist = 0
		estimatedAngle = 0
		for k in range(0,len(array)):
			if k != index:
				 estimatedAngle += array[k]
		
		estimatedAngle /= (len(array)-1)
		return estimatedAngle
	else:
		estimatedAngle = 0
		for item in array:
 			estimatedAngle += item
		estimatedAngle /= len(array)
		return estimatedAngle

def FindJump(array):
	up = 0
	down = 0
	for item in array:
		if item>0:
			up += 1
		else:
			down += 1
	if up == 0 or down == 0:
		return array
	else:
		if up >= down:
			return SetOrientation(array,1)
		else:
			return SetOrientation(array,-1)
				
def SetOrientation(array,ori):		
	index = 0
	for item in array:
		array[index] = ori * abs(item)
		index += 1
	return array
		

