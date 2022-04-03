###############
##Design the function "calibrate" to  return 
# (1) intrinsic_params: should be a list with four elements: [f_x, f_y, o_x, o_y], where f_x and f_y is focal length, o_x and o_y is offset;
# (2) is_constant: should be bool data type. False if the intrinsic parameters differed from world coordinates. 
#                                            True if the intrinsic parameters are invariable.
#It is ok to add other functions if you need
###############
import numpy as np
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, TERM_CRITERIA_EPS, TERM_CRITERIA_MAX_ITER, \
    findChessboardCorners, cornerSubPix, drawChessboardCorners

def calibrate(imgname):
    #......
    criteria = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 30, 0.001)

    checkboardpoints = np.array([[40,0,40],[40,0,30],[40,0,20],[40,0,10],[30,0,40],[30,0,30],[30,0,20],[30,0,10],
                           [20,0,40],[20,0,30],[20,0,20],[20,0,10],[10,0,40],[10,0,30],[10,0,20],[10,0,10],
                           [0,10,40],[0,10,30],[0,10,20],[0,10,10],[0,20,40],[0,20,30],[0,20,20],[0,20,10],
                           [0,30,40],[0,30,30],[0,30,20],[0,30,10],[0,40,40],[0,40,30],[0,40,20],[0,40,10]])
    wobjpoints = []
    imgpoints = [] 

    img = imread(imgname)
    gray = cvtColor(img,COLOR_BGR2GRAY)

   
    ret,corners=findChessboardCorners(gray,(4,9),None)
    

    if ret == True:
        wobjpoints.append(checkboardpoints)
        for i in range (0,4):
            corners  = np.delete(corners,16,axis=0)
        
        corners2 = cornerSubPix(gray,corners,(4,4),(-1,-1),criteria)
        
        imgpoints.append(corners2)
        
        img = drawChessboardCorners(img, (4,4), corners2[0:15,:,:],ret)
        img = drawChessboardCorners(img, (4,4), corners2[16:31,:,:],ret)
       
    else:
        print ("Corners not found")
        

    worldpoints=wobjpoints[0]   
    imagepoints=imgpoints[0]
    imagepoints = imagepoints.reshape((imagepoints.shape[0]*imagepoints.shape[1]), imagepoints.shape[2])
    
    worldr,worldc=worldpoints.shape
    imager,imagec=imagepoints.shape
     
    n=worldr 
    ProjMat=np.zeros((2*n,12))
    
    for i in range(n):
        
        X,Y,Z=worldpoints[i]
        x,y=imagepoints[i]
        
        eqn1 = np.array([  X,  Y,  Z,  1,  0,  0,  0,  0, -(X*x), -(Y*x), -(Z*x), -(x)])
        eqn2 = np.array([  0,  0,  0,  0,  X,  Y,  Z,  1, -(X*y), -(Y*y), -(Z*y), -(y)])
        ProjMat[2*i] = eqn1
        ProjMat[(2*i) + 1] = eqn2

    
    U, S, VT = np.linalg.svd(ProjMat)
    x=VT[-1]
    print (x)
    lambdaa=np.sqrt(1/np.sum(x[8:11]*x[8:11]))
    mmatrix=lambdaa*x    
    mmatrix=mmatrix.reshape(3,4)
  
    m3 = np.transpose((mmatrix[2,0:3]))
    
    ox1 = (mmatrix[0,0:3]).dot(m3)
    oy1 = (mmatrix[1,0:3]).dot(m3)

    ox = ox1.item()
    oy = oy1.item()
    
    m1 = np.transpose((mmatrix[0,0:3]))
    
    m2 = np.transpose((mmatrix[1,0:3]))

    fx=np.sqrt(np.sum((m1.dot(mmatrix[0,0:3]))-(ox*ox)))
                
    fy=np.sqrt(np.sum((m2.dot(mmatrix[1,0:3]))-(oy*oy)))

    intrinsic_params=[fx,fy,ox,oy]
    
    return intrinsic_params,True
       
    
if __name__ == "__main__":
    intrinsic_params, is_constant = calibrate('checkboard.png')
    print(intrinsic_params)
    print(is_constant)
