
from PIL import Image
import final_stitch
import os
import pygame
from tqdm import tqdm
B_path= os.path.dirname(os.path.abspath(__file__))

foreground_list=[['elon/elon-foregrounds1.png','elon/elon-foregrounds2.png','elon/elon-foregrounds3.png','elon/elon-foregrounds4.png'],['elon/rupi-foregrounds1.png','elon/rupi-foregrounds2.png','elon/rupi-foregrounds3.png','elon/rupi-foregrounds4.png'],['elon/meme-foregrounds1.png','elon/meme-foregrounds2.png','elon/meme-foregrounds3.png','elon/meme-foregrounds4.png']]

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

def process(img, id,mode,select):
    
    foreground = Image.open(foreground_list[int(select)][id])
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


def filter(input_list,temp,mode):
    # print(input_list)
    processed = []
    if mode ==elon:
        mode_s=0
    elif mode ==rupi:
        mode_s=1
    elif mode ==meme:
        mode_s=2
    for i in tqdm(range(len(input_list))):
        processed.append(process(input_list[i],i,1,mode_s))
    
    # print(processed)

    return final_stitch.stitch(processed,temp)

# filter(['desk/1.png','desk/2.png','desk/3.png','desk/4.png'])
print("[*]ELON-ready to go")