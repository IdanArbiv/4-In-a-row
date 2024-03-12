import numpy as np
from skimage import transform

def PerformHomography(Im, p, p2):
    A = np.zeros((8, 8))
    b = np.zeros((8, 1))
    for i in range(4):
        A[(i*2), :] = [p[i,0], p[i,1], 1, 0, 0, 0, -p[i,0]*p2[i,0], -p[i,1]*p2[i,0]]
        A[(i*2)+1, :] = [0, 0, 0, p[i,0], p[i,1], 1, -p[i,0]*p2[i,1], -p[i,1]*p2[i,1]]
        b[(i*2)] = p2[i,0]
        b[(i*2)+1] = p2[i,1]
    h = np.linalg.solve(A, b)
    H = np.array([[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1]])
    TFORM = transform.ProjectiveTransform(matrix=H)
    Im_rectified = transform.warp(Im, TFORM)
    Im_rectified_temp = np.zeros_like(Im_rectified)
    Im_rectified_temp[:,:,0] = Im_rectified[:,:,0].T
    Im_rectified_temp[:,:,1] = Im_rectified[:,:,1].T
    Im_rectified_temp[:,:,2] = Im_rectified[:,:,2].T
    return Im_rectified_temp

