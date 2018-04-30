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
from m_util import *
from vis import *
opt = TestOptions().parse()
#opt = argparse.ArgumentParser().parse_args()
#opt.im_fold='/gpfs/projects/LynchGroup/Train_all/CROPPED/p1000/'
#opt.im_fold = '/nfs/bigbox/hieule/penguin_data/CROPPED/p300/'
#opt.im_fold ='/nfs/bigbox/hieule/penguin_data/Test/CROZ/CROPPED/p300/'
opt.checkpoints_dir = '/nfs/bigbox/hieule/penguin_data/checkpoints_new/'
opt.name = 'train_on_p300'
opt.name = 'MSEnc3_p2000_train_bias0.5_bs128'
#opt.name ='MSE_mb_p500_train_bias0.5_bs128'
opt.input_nc =3
opt.model = 'single_unet'
opt.step = 64
opt.size = 256
opt.test = True
opt.no_dropout = True
#name = ['MSEnc3_train1_all_bias0.2_bs128'
#,'MSEnc3_train10.75_0_bias0.2_bs128',
#'MSEnc3_train10.5_0_bias0.2_bs128',
#'MSEnc3_train10.25_0_bias0.2_bs128'
#        ]
def read_list(f):
    if os.path.isfile(f):
        file = open(f,"r")
        a= file.read()
        traininglist =  a.split("$")
        del traininglist[-1]
        return traininglist
    return []

def do_the_thing_please(opt):
    opt.patch_fold_res = opt.im_fold + 'PATCHES/res/' + opt.name+ '/'
    opt.im_res = opt.im_fold + 'res/' + opt.name +'e'+str(opt.which_epoch)+'/'
    
    opt.patch_fold = opt.im_fold+'PATCHES/'+str(opt.step)+'_'+ str(opt.size)
    opt.patch_fold_A = opt.im_fold+'PATCHES/'+str(opt.step)+'_'+ str(opt.size)+ '/A/'
    opt.patch_fold_B = opt.im_fold+'PATCHES/'+str(opt.step)+'_'+ str(opt.size)+'/B/'
    A_fold = opt.im_fold + 'A/'
    B_fold = opt.im_fold +  'B/'
    sdmkdir(opt.patch_fold_A)
    sdmkdir(opt.patch_fold_B)
    sdmkdir(opt.patch_fold_res)
    sdmkdir(opt.im_res)
    imlist=[]
    imnamelist=[]
    
    
    opt.dataset_mode ='png_withlist'
    opt.nThreads = 2
    opt.fineSize = 256
    opt.loadSize = 256
    opt.biased_sampling = -0.5
    opt.batchSize = 32
    opt.max_dataset_size = 5000000
    opt.no_flip = True
    opt.serial_batches = False
    #opt.dataroot = '/nfs/bigbox/hieule/penguin_data/MB_Same_Size/Train/Train_all/CROPPED/p500_train/PATCHES/64_386/'
    opt.dataroot = opt.patch_fold
    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    print(len(dataset))
    

    for i,data in enumerate(dataset):
        print data['A'].shape
        temp = model.get_prediction(data)['raw_out']
        print temp.shape
        for k in range(0,temp.shape[0]):
            misc.toimage(temp[k,:,:,0],mode='L').save(os.path.join(opt.patch_fold_res,data['imname'][k]))
    imlist=[]
    imnamelist=[]
    traininglist = read_list(opt.traininglist)
    for root,_,fnames in sorted(os.walk(A_fold)):
        for fname in fnames:
            if fname.endswith('.png') and "M1BS" in fname and fname[:-4] in traininglist:
                path = os.path.join(root,fname)
                path_mask = os.path.join(B_fold,fname)
                imlist.append((path,path_mask,fname))
                imnamelist.append(fname)
    for im_path,mask_path,imname in  imlist:
        png = misc.imread(im_path,mode='RGB')
        w,h,z = png.shape
        mask = patches2png(opt.patch_fold_res,imname,w,h,opt.step,opt.size)
        misc.toimage(mask.astype(np.uint8),mode='L').save(os.path.join(opt.im_res,imname))

name = [
'MSEnc3_train0.8_0_bias-1_bs128',
'MSEnc3_train_0_0.5_0_bias-1_bs128',
'MSEnc3_train_0_0.75_0_bias-1_bs128',
'MSEnc3_train_0_0.25_0_bias-1_bs128'
]

def list2file(li,fi):
    file = open(fi,"w")
    for i in li:
        for j in i:
            file.write(str(j))
            file.write("  ")
        file.write("\n")
    file.close()

for epoch in [2]:
    opt.which_epoch = epoch 
    for i in [1,2,3,4]:
        opt.traininglist = '/nfs/bigbox/hieule/penguin_data/p1000/split/test_' + str(i)
        traininglist = read_list(opt.traininglist)
        opt.name =  'MSEnc3_train0.8_'+str(i)+'_bias-1_bs128'
        model = create_model(opt)
        opt.im_fold = '/nfs/bigbox/hieule/penguin_data/p1000/'
        do_the_thing_please(opt)
        visABC(opt.im_fold,opt.name+'e'+str(opt.which_epoch),imlist = traininglist )
        auc = AUC(opt.im_fold,opt.name+'e'+str(opt.which_epoch),pimlist = traininglist )
        list2file(auc,'./AUC/'+opt.name+'_e'+str(epoch)+'.txt')
    #    visAB(opt.im_fold,opt.name+'e'+str(opt.which_epoch),imlist = traininglist)

#opt.im_fold ='/nfs/bigbox/hieule/penguin_data/CROPPED/p500_train/'
#do_the_thing_please(opt)
#opt.im_fold_temp ='/nfs/bigbox/hieule/penguin_data/Test/*TEST*/CROPPED/p300/'
#for t in ["PAUL","CROZ"]:
#    opt.im_fold = opt.im_fold_temp.replace("*TEST*",t)
#    do_the_thing_please(opt)
