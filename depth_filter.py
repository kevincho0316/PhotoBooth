import cv2
import torch
import numpy as np

#######################
# process('/content/gfdud33u33.jpg', 1 )
##########################
data_list=[ ['depth/img/to_the_moon/background.png',400,-15,(346, 95),'depth/img/to_the_moon/forground.png'],
            ['depth/img/to_the_moon/background.png',400,-15,(346, 95),'depth/img/to_the_moon/forground.png'],
            ['depth/img/to_the_moon/background.png',400,-15,(346, 95),'depth/img/to_the_moon/forground.png'],
            ['depth/img/to_the_moon/background.png',400,-15,(346, 95),'depth/img/to_the_moon/forground.png'],
            
            
            ]

def place(img, id):
    
    people = Image.open(img)
    foreground = Image.open(data_list[id-1][4])
    people.thumbnail((data_list[id-1][1],data_list[id-1][1])) #한변의 최대 길이
    fw, fh = people.size
    people = people.rotate(data_list[id-1][2],expand=True)
    

    background = Image.open(data_list[id-1][0])
    
    

    # print(m)
    background.paste(people,data_list[id-1][3],people)
    background.paste(foreground,(0,0),foreground)
    out_dir = 'depth/output/'+img.split('/')[-1].split('.')[0]+'.jpg'
    background = background.convert("RGB")
    background.save(out_dir)



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
    np.save('/content/depth/depth_result/'+filedir.split('/')[-1].split('.')[0]+'.npy',output)


    frame = cv2.imread(filedir, 0)

    cut = 20
    output[output < cut] = 0
    output[output > cut] = 255



    # output.size
    mask = output == 0
    resizedOrig = cv2.resize(frame, mask.shape[1::-1])
    resizedOrig.shape
    resizedOrig[mask] = 0
    cv2.imwrite('/content/depth/depth_result_cut/'+filedir.split('/')[-1].split('.')[0]+'.jpg', resizedOrig)
    
    place('/content/depth/depth_result_cut/'+filedir.split('/')[-1].split('.')[0]+'.jpg',id)
    
    torch.cuda.empty_cache()
    return '/content/depth/output/'+filedir.split('/')[-1].split('.')[0]+'.jpg'

def filter(img1,img2,img3,img4):
    processed = []
    processed.append(process(img1,1))
    processed.append(process(img2,2))
    processed.append(process(img3,3))
    processed.append(process(img4,4))

    print(processed)

    return final_stitch.stitch(processed)