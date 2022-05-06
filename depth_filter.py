import cv2
import time
import torch
import final_stitch
#######################
# process('/content/gfdud33u33.jpg', 1 )
##########################

def stitch(img_list, interpolation 
                   = cv2.INTER_CUBIC):
      # take minimum width

    out = '/content/product/'

    img_readed = []
    for img in img_list:
        img_readed.append(cv2.imread(img))

    w_min = min(img.shape[1] 
                for img in img_readed)
      
    # resizing images
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
                      for img in img_readed]

    img_v_resize = cv2.vconcat(im_list_resize)
    # return final image
    out_dir = out + img_list[0].split('/')[-1].split('.')[0][0:-2]+'.jpg'
    cv2.imwrite(out_dir, img_v_resize)
    return out_dir

import cv2
import torch

#######################
# process('/content/gfdud33u33.jpg', 1 )
##########################

def process(filedir, id):
    model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
    # model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
    #model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

    midas = torch.hub.load("intel-isl/MiDaS", model_type)

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
        transform = midas_transforms.dpt_transform
    else:
        transform = midas_transforms.small_transform

    img = cv2.imread(filedir)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    # plt.imshow(output)


    frame = cv2.imread(filedir, 0)

    cut = 20
    output[output < cut] = 0
    output[output > cut] = 255



    # output.size
    mask = output == 0
    resizedOrig = cv2.resize(frame, mask.shape[1::-1])
    resizedOrig.shape
    resizedOrig[mask] = 0
    cv2.imwrite('/content/depth/depth_result/'+filedir.split('/')[-1].split('.')[0]+'.jpg', resizedOrig)

    if id == 1:
        print()
    elif id == 2:
        print()
    elif id == 3:
        print()
    elif id == 4:
        print()
    
    torch.cuda.empty_cache()
    return '/content/depth/depth_result/'+filedir.split('/')[-1].split('.')[0]+'.jpg'

def filter(img1,img2,img3,img4):
    processed = []
    processed.append(process(img1,1))
    processed.append(process(img2,2))
    processed.append(process(img3,3))
    processed.append(process(img4,4))

    print(processed)

    return final_stitch.stitch(processed)