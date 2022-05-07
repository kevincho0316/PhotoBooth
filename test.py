
from PIL import Image
import final_stitch

data_list=[ ['depth/img/doge_mountain/background.png',600,0,(277, 70),'depth/img/doge_mountain/foreground.png'],
            ['depth/img/light_travel/background.png',450,0,(330, 100),'depth/img/light_travel/foreground.png'],
            ['depth/img/radioactive_pool/background.png',500,0,(190, 189),'depth/img/radioactive_pool/foreground.png'],
            ['depth/img/to_the_moon/background.png',450,-15,(320, 35),'depth/img/to_the_moon/foreground.png'],
            ]
def process(img, id):
    
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