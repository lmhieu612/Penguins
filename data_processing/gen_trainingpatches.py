from models.models import create_model
from data.png_dataset import PngDataset
import numpy as np
from PIL import Image 
from options.train_options import TrainOptions
from options.test_options import TestOptions
import time
from data.data_loader import CreateDataLoader
import torch
import os.path
import argparse
from scipy import misc
from vis import visAB,visABC
from m_util import *
parse = argparse.ArgumentParser()
parse.add_argument('--dataset')
opt = parse.parse_args()
opt.root = '/gpfs/projects/LynchGroup/Penguin_workstation/Train_all/fullsize/'
#opt.root = '/nfs/bigbox/hieule/penguin_data/p1000/'
#opt.im_fold_temp ='/nfs/bigbox/hieule/penguin_data/Test/*TEST*/CROPPED/p300/'
#for t in ["PAUL","CROZ"]:
#opt.im_fold = opt.im_fold_temp.replace("*TEST*",t)
opt.im_fold = opt.root
opt.step = 512 #128 for testing, 64 for training
opt.size = 768 #256 for testing, 386 for training
opt.patch_fold_A = opt.im_fold+'PATCHES/'+str(opt.step)+'_'+ str(opt.size)+ '/A/'
opt.patch_fold_B = opt.im_fold+'PATCHES/'+str(opt.step)+'_'+ str(opt.size)+'/B/'
A_fold = opt.im_fold + 'A/'
B_fold = opt.im_fold +  'B/'

opt.input_nc =3
sdmkdir(opt.patch_fold_A)
sdmkdir(opt.patch_fold_B)
imlist=[]
todolist=[]
#todolist = read_list('/nfs/bigbox/hieule/penguin_data/p1000/split/test_new')
print(todolist)
imnamelist=[]

for root,_,fnames in sorted(os.walk(A_fold)):
    for fname in fnames:
        if fname.endswith('.png') and 'M1BS' in fname and (fname[:-4] in todolist or len(todolist)==0):
            path = os.path.join(root,fname)
            path_mask = os.path.join(B_fold,fname)
            imlist.append((path,path_mask,fname))
            imnamelist.append(fname)
for im_path,mask_path,imname in  imlist:
    png = misc.imread(im_path,mode='RGB')
    print(mask_path)
    mask = misc.imread(mask_path)
    print(mask.shape)
    w,h,z = png.shape
    savepatch_train(png,mask,w,h,opt.step,opt.size,opt.patch_fold_A+'/'+imname[:-4]+'#',opt.patch_fold_B+'/'+imname[:-4]+'#')