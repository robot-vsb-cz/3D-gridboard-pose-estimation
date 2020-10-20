import numpy as np
import numpy
import math
from numpy.linalg import inv

# Z Eulerovych uhlu vytvori rotacni matici
def eulerAnglesToRotationMatrix(theta) :
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    return np.dot(R_x, np.dot( R_y, R_z ))

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
 
 
# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    x = -math.atan2(R[1,2] , R[2,2])
    y = -math.atan2(-R[0,2] , math.sqrt(R[0,0] * R[0,0] +  R[0,1] * R[0,1]))
    z = -math.atan2(R[0,1] , R[0,0])
    
    return np.array([x, y, z])

# Vytvori 4x4 matici ze submatice rotace a translace
def Create4x4Mat(submat,tvec):
    mat = np.matrix([[ submat[0,0],   submat[0,1],   submat[0,2],    tvec[0]],
                     [ submat[1,0],   submat[1,1],   submat[1,2],    tvec[1]],
                     [ submat[2,0],   submat[2,1],   submat[2,2],    tvec[2]],
                     [           0,             0,             0,         1]])
    return mat
       
# Vrati inverzni matici
def InversMatrix(m):
    return inv(m)

def RoundMatrix(m):
    for i in range(0, 4):
        for j in range(0, 4):
            m[i,j] = round(m[i,j],5)

    return m
# Vrati submatici rotace
def GetSubmat(R):
    finalSubmat = np.matrix([[R[0,0],   R[0,1],   R[0,2]],
                             [R[1,0],   R[1,1],   R[1,2]],
                             [R[2,0],   R[2,1],   R[2,2]]])
    return finalSubmat


def GetTvec(mat):
	tvec = [0]*3
	tvec[0] = mat[0,3]
	tvec[1] = mat[1,3] 
	tvec[2] = mat[2,3]
	return tvec

