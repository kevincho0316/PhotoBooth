#@title Anime FaceGAN Colab app
from io import BytesIO
import os
import torch
from PIL import Image
import final_stitch
import ipywidgets as widgets
from tqdm import tqdm
B_path= os.path.dirname(os.path.abspath(__file__))


device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", device=device).eval()
face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", size=1080 ,device=device)
image_format = "png"

button = widgets.Button(description="Start")
output = widgets.Output()
        



def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


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
        processed.append(process(input_list[i]))
    
    # print(processed)

    return final_stitch.stitch(processed)

def crop(im): # opend im 
    new_width = 1080
    new_height = 720
    width, height = im.size   # Get dimensions

    left = 0
    top = 0
    right = 1080
    bottom = 720

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    return im

def process(img):
    createFolder(B_path+'/anime/output/'+img.split('/')[-2].replace('.',''))
    im_in = Image.open(img).convert("RGB")
    padding = Image.open(B_path+'/depth/img/white.jpg').resize((1080,360))
    padded = get_concat_v(im_in,padding)

    im_out = face2paint(model, padded, side_by_side=False)
    im_out = crop(im_out)
    buffer_out = BytesIO()
    out_dir = B_path+'/anime/output/'+img.split('/')[-2].replace('.','')+"/"+img.split('/')[-1].split('.')[0]+'.jpg'
    im_out.save(buffer_out, format=image_format)
    im_out.save(out_dir)
    
    bytes_out = buffer_out.getvalue()
    return out_dir





# filter(['desk/1.png','desk/2.png','desk/3.png','desk/4.png'])
print("[*]ANIME-ready to go")