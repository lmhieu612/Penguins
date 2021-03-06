
def create_model(opt):
    model = None
    print(opt.model)
    if opt.model == 'cycle_gan':
        assert(opt.dataset_mode == 'unaligned')
        from .cycle_gan_model import CycleGANModel
        model = CycleGANModel()

    elif opt.model == 'single_unet_mb':
        from .single_unet_mb import UnetModel
        model = UnetModel()
    elif opt.model == 'single_unet_4c':
        from .single_unet_4c import UnetModel
        model = UnetModel()
    elif opt.model == 'vusingle_unet':
        from .vusingle_unet import UnetModel
        model = UnetModel()
    elif opt.model == 'single_unet':
        from .single_unet import UnetModel
        model = UnetModel()
    elif opt.model == 'sdrm_pix2pix':
        from .sdrm_pix2pix_model import SDRMPix2PixModel
        model = SDRMPix2PixModel()
    elif opt.model == 'pix2pix':
        assert(opt.dataset_mode == 'aligned')
        from .pix2pix_model import Pix2PixModel
        model = Pix2PixModel()
    elif opt.model == 'test':
        assert(opt.dataset_mode == 'single')
        from .test_model import TestModel
        model = TestModel()
    else:
        raise ValueError("Model [%s] not recognized." % opt.model)
    model.initialize(opt)
    print("model [%s] was created" % (model.name()))
    return model
