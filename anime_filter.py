#@title Anime FaceGAN Colab app

from io import BytesIO
import torch
from PIL import Image
import final_stitch
import ipywidgets as widgets
from tqdm import tqdm


device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", device=device).eval()
face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", size=540 ,device=device)
image_format = "png"

button = widgets.Button(description="Start")
output = widgets.Output()
        

def process(img):
    createFolder(B_path+'/anime/output/'+img.split('/')[-2].replace('.',''))
    im_in = Image.open(img).convert("RGB")
    im_out = face2paint(model, im_in, side_by_side=True)
    buffer_out = BytesIO()
    im_out.save(buffer_out, format=image_format)
    bytes_out = buffer_out.getvalue()

    

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def filter(input_list):
    # print(input_list)
    processed = []
    for i in tqdm(range(len(input_list))):
        processed.append(process(input_list[i],i,1))
    
    # print(processed)

    return final_stitch.stitch(processed)

# filter(['desk/1.png','desk/2.png','desk/3.png','desk/4.png'])
print("[*]ANIME-ready to go")