# from typing import final
import cv2

# define a function for vertically 
# concatenating images of different
# widths 
def stitch(img_list, interpolation 
                   = cv2.INTER_CUBIC):
      # take minimum width

    out = 'content/product/'

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

# print(stitch(['elon/backgrounds.png', 'elon/foregrounds.png', 'elon/l_2021071602000853400181201-1.jpg', 'elon/mask.png']))

