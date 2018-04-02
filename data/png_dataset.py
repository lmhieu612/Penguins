import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
from PIL import ImageFilter
import torch
from pdb import set_trace as st
import random
import numpy as np
import time
from scipy import misc
import cv2
class PngDataset(BaseDataset):
    def __init__(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.GTroot = opt.dataroot
        self.A_dir = opt.dataroot + '/A/'
        self.B_dir = opt.dataroot + '/B/'
        self.imname = []
        self.imname_pos = []
        for root,_,fnames in sorted(os.walk(self.A_dir)):
            for fname in fnames:
                if fname.endswith('.png'):
                    path = os.path.join(root,fname)
                    self.imname.append(fname)
        
        for root,_,fnames in sorted(os.walk(self.B_dir)):
            for fname in fnames:
                if fname.endswith('.png'):
                    path = os.path.join(root,fname)
                    self.imname_pos.append(fname)
        self.nim = len(self.imname)

    def __len__(self):
        return 50000
        #return self.nim*20
    def name(self):
        return 'PNGDATASET'
    
    def getpatch(self,idx,i,j):
        A_img = self.tifimg[:,i*256:(i+1)*256,j*256:(j+1)*256]
        B_img = self.GTmask[:,i*256:(i+1)*256,j*256:(j+1)*256]
        A_img = torch.from_numpy(A_img).float().div(255)
        B_img = torch.from_numpy(B_img).float().div(255)
        
        A_img = torch.unsqueeze(A_img,0)
        B_img = torch.unsqueeze(B_img,0)
        return  {'A': A_img, 'B': B_img,'imname':self.imname[0]}
    def get_number_of_patches(self,idx):
        return self.nx,self.ny
    def __getitem__(self,index):
        if random.random() < self.opt.biased_sampling:
            r_index = index % len(self.imname_pos)
            imname = self.imname_pos[r_index]
            A_img = np.asarray(Image.open(os.path.join(self.A_dir,imname)))
            B_img = np.asarray(Image.open(os.path.join(self.B_dir,imname)))
        else:
            
            r_index = index % len(self.imname)
            imname = self.imname[r_index]
            A_img = np.asarray(Image.open(os.path.join(self.A_dir,imname)))
            
            if imname in self.imname_pos:
                B_img = np.asarray(Image.open(os.path.join(self.B_dir,imname)))
            else:
                t = A_img.shape
                B_img = np.zeros((A_img.shape[0],A_img.shape[1]))
        
        C_img = np.copy(B_img).astype(np.uint8)
        C_img = cv2.dilate(C_img, np.ones((30,30)))
        C_img[C_img>0] = 255
        A_img = np.transpose(A_img,(2,0,1))
        B_img = np.expand_dims(B_img, axis=0)
        C_img = np.expand_dims(C_img, axis=0)
        z,w,h = A_img.shape
        w_offset = random.randint(0,max(0,w-self.opt.fineSize-1))
        h_offset = random.randint(0,max(0,h-self.opt.fineSize-1))
        A_img = A_img[:, w_offset:w_offset + self.opt.fineSize, h_offset:h_offset + self.opt.fineSize] 
        B_img = B_img[:,w_offset:w_offset + self.opt.fineSize, h_offset:h_offset + self.opt.fineSize]
        C_img = C_img[:,w_offset:w_offset + self.opt.fineSize, h_offset:h_offset + self.opt.fineSize]
        A_img = torch.from_numpy(A_img).float().div(255)
        B_img = torch.from_numpy(B_img).float().div(255)
        C_img = torch.from_numpy(C_img).float().div(255)
        A_img = A_img - 0.5
        A_img = A_img * 2
        return  {'A': A_img, 'B': B_img,'C':C_img}