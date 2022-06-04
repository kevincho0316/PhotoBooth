
from PIL import Image
import final_stitch
import os
import pygame
from tqdm import tqdm
B_path= os.path.dirname(os.path.abspath(__file__))

foreground_list=['elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png']

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

def process(img, id,mode):
    
    foreground = Image.open(foreground_list[id])
    if mode ==1:
        background = Image.open(img)
    else:
        background = img

    bw, bh = background.size
    fw, fh = foreground.size
    foreground.thumbnail(background.size)
    m= int(fw/2)

    # print(bw)
    # print(m)

    background.paste(foreground,(round((bw/2 - m)), bh-fh),foreground)
    if mode == 0:
        background.resize((1080,720))
        return pilImageToSurface(background)
    elif mode == 1:
        createFolder(B_path+'/elon/output/'+img.split('/')[-2].replace('.',''))
        out_dir = B_path+'/elon/output/'+img.split('/')[-2].replace('.','')+"/"+img.split('/')[-1].split('.')[0]+'.jpg'
        background = background.convert("RGB")
        background.resize((1080,720))
        background.save(out_dir)
        return out_dir

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
print("[*]ELON-ready to go")