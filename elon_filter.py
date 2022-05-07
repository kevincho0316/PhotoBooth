
from PIL import Image
import final_stitch

foreground_list=['elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png','elon/foregrounds.png']

def process(img, id):
    
    foreground = Image.open(foreground_list[id-1])
    background = Image.open(img)

    bw, bh = background.size
    fw, fh = foreground.size
    m= int(fw/2)

    # print(bw)
    # print(m)

    background.paste(foreground,(round((bw/2 - m)), bh-fh),foreground)
    out_dir = 'elon/output/'+img.split('/')[-1].split('.')[0]+'.jpg'
    background = background.convert("RGB")
    background.save(out_dir)
    return out_dir


def filter(img1,img2,img3,img4):
    processed = []
    processed.append(process(img1,1))
    processed.append(process(img2,2))
    processed.append(process(img3,3))
    processed.append(process(img4,4))

    print(processed)

    return final_stitch.stitch(processed)

filter('test/324-1.png','test/324-2.png','test/324-3.png','test/324-4.png')