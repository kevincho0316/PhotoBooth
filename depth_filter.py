import cv2
from PIL import Image
import torch
import numpy as np
import final_stitch
import os
B_path= os.path.dirname(os.path.abspath(__file__))


#######################
# process('/content/gfdud33u33.jpg', 1 )
##########################
data_list=[ ['depth/img/doge_mountain/background.png',600,0,(277, 70),'depth/img/doge_mountain/foreground.png'],
            ['depth/img/light_travel/background.png',450,0,(330, 100),'depth/img/light_travel/foreground.png'],
            ['depth/img/radioactive_pool/background.png',500,0,(190, 189),'depth/img/radioactive_pool/foreground.png'],
            ['depth/img/to_the_moon/background.png',450,-15,(320, 35),'depth/img/to_the_moon/foreground.png'],
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
    out_dir = B_path +'/depth/output/'+img.split('/')[-1].split('.')[0]+'.jpg'
    background = background.convert("RGB")
    background.save(out_dir)
    return out_dir

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
    np.save(B_path+'/depth/depth_result/'+filedir.split('/')[-1].split('.')[0]+'.npy',output)


    frame = cv2.imread(filedir, 0)

    cut = 20
    output[output < cut] = 0
    output[output > cut] = 255



    # output.size
    mask = output == 0
    resizedOrig = cv2.resize(frame, mask.shape[1::-1])
    resizedOrig.shape
    resizedOrig[mask] = 0
    cv2.imwrite(B_path+'/depth/depth_result_cut/'+filedir.split('/')[-1].split('.')[0]+'.jpg', resizedOrig)
    
    place(B_path+'/depth/depth_result_cut/'+filedir.split('/')[-1].split('.')[0]+'.jpg',id)
    
    torch.cuda.empty_cache()
    return B_path+'/depth/output/'+filedir.split('/')[-2:-1].split('.')[0]+'.jpg'


def filter(input_list):
    print(input_list)
    processed = []
    for i in range(len(input_list)):
        processed.append(process(input_list[i],i))
    
    print(processed)

    return final_stitch.stitch(processed)


filter('test/324-1.png','test/324-2.png','test/324-3.png','test/324-4.png')
print("[*]DEPTH-ready to go")