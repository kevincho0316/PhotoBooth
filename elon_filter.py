
from PIL import Image
import final_stitch
import os
B_path= os.path.dirname(os.path.abspath(__file__))

foreground_list=['elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png']

def process(img, id):
    
    foreground = Image.open(foreground_list[id])
    background = Image.open(img)

    bw, bh = background.size
    fw, fh = foreground.size
    m= int(fw/2)

    # print(bw)
    # print(m)

    background.paste(foreground,(round((bw/2 - m)), bh-fh),foreground)
    out_dir = B_path+'/elon/output/'+img.split('/')[-2:-1].split('.')[0]+'.jpg'
    background = background.convert("RGB")
    background.save(out_dir)
    return out_dir


def filter(input_list):
    print(input_list)
    processed = []
    for i in range(len(input_list)):
        processed.append(process(input_list[i],i))
    
    print(processed)

    return final_stitch.stitch(processed)

# filter('test/324-1.png','test/324-2.png','test/324-3.png','test/324-4.png')
print("[*]ELON-ready to go")