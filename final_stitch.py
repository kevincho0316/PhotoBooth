# from typing import final
# import cv2

# define a function for vertically 
# concatenating images of different
# widths 

# def stitch(img_list, interpolation 
#                    = cv2.INTER_CUBIC):
#       # take minimum width

#     out = '/contentproduct/'


#     img_readed = []
#     for img in img_list:
#         img_readed.append(cv2.imread(img))

#     w_min = min(img.shape[1] 
#                 for img in img_readed)
      
#     # resizing images
#     im_list_resize = [cv2.resize(img,
#                       (w_min, int(img.shape[0] * w_min / img.shape[1])),
#                                  interpolation = interpolation)
#                       for img in img_readed]

#     img_v_resize = cv2.vconcat(im_list_resize)
#     # return final image
#     out_dir = out + img_list[0].split('/')[-1].split('.')[0][0:-2]+'.jpg'
#     cv2.imwrite(out_dir, img_v_resize)
#     return out_dir


from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask

ip = 'http://104.197.148.203:8080'

def stitch(images_list):
    imgs = [Image.open(i) for i in images_list]
    plate = Image.open('final_stitch/plate-v2-f.png')

    # If you're using an older version of Pillow, you might have to use .size[0] instead of .width
    # and later on, .size[1] instead of .height
    min_img_width = min(i.width for i in imgs)

    total_height = 0
    for i, img in enumerate(imgs):
        # If the image is larger than the minimum width, resize it
        if img.width > min_img_width:
            imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
        total_height += imgs[i].height

    # I have picked the mode of the first image to be generic. You may have other ideas
    # Now that we know the total height of all of the resized images, we know the height of our final image
    
    img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
    y = 0
    for img in imgs:
        img_merge.paste(img, (0, y))

        y += img.height
    
    plate.paste(img_merge,(72,278))
  
    out_dir = 'product/' + images_list[0].split('/')[-1].split('.')[0][0:-2]+'.jpg'
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0.1,
        )
    # qr.add_data('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    qr.add_data(ip+'/'+out_dir)

    qr_img = qr.make_image(image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer())
    # img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
    qr_s = 120
    qr_img = qr_img.resize((qr_s,qr_s))
    plate.paste(qr_img,(612-int(qr_s/2),3470))
    final = plate.convert("RGB")
    final.save(out_dir)
    return out_dir



