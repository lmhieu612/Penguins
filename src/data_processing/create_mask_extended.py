import os
import numpy as np
from scipy import misc
import matplotlib as plt
import cv2
root = '/nfs/bigbox/hieule/GAN/'
rA = root + 'TrainA/'
rB = root + 'TrainB/'
rC = root + 'TrainC/'
def sdmkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
augroot = '/nfs/bigbox/hieule/GAN/datasets/SBUsd/Train4K/TrainC/'
sdmkdir(augroot)
ker = np.ones((5,5),np.uint8)
for r,_,fnames in os.walk(root+'TrainB'):
    for fname in fnames:
        if fname.endswith('png'):
            B = misc.imread(os.path.join(rB,fname.replace('jpg','png')),mode='RGB')
            print B.shape
            print B.shape
            B_ero = cv2.erode(B,np.ones((7,7),np.uint8))
            B_dil = cv2.dilate(B,np.ones((5,5),np.uint8))
            B_ero[B_ero<255] = 0
            B_dil[B_dil>0] = 255
            savim = np.ones(B.shape,np.uint8)

            savim[(B-B_ero)>0] = 0
            savim[(B_dil - B)>0] = 2
            cv2.imwrite(augroot + fname, savim)
            
            #misc.toimage(A).save(os.path.join(augrootA,'aug1.2_'+fname))
            #misc.toimage(misc.imread(os.path.join(rB,fname.replace('jpg','png')))).save(os.path.join(augrootB,'aug1.2_'+fname.replace('jpg','png')))
