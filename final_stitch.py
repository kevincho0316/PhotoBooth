
from PIL import Image, ImageEnhance
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
import socket
ip = 'http://'+'metash.p-e.kr'+':8080'

def crop(im): # opend im 
    new_width = 1080
    new_height = 720
    width, height = im.size   # Get dimensions

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    return im


def stitch(images_list):
    imgs = [Image.open(i) for i in images_list]
    plate = Image.open('final_stitch/plate-v3-f.png')

    # If you're using an older version of Pillow, you might have to use .size[0] instead of .width
    # and later on, .size[1] instead of .height
    min_img_width = min(i.width for i in imgs)

    total_height = 0
    for i, img in enumerate(imgs):
        img = crop(img)
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
    
    top = 324
    bottom = 3185
    gap = 72
 
    paste_cor_y = int((((bottom-top)/2)+top)-(img_merge.height/2))
    paste_cor_x = int((plate.width/2)-(img_merge.width/2))
    plate.paste(img_merge,(paste_cor_x,paste_cor_y))
  
    out_dir = 'product/' + images_list[0].split('/')[-2].split('.')[0]+'.jpg'
    qr_dir = 'p/' + images_list[0].split('/')[-2].split('.')[0]+'.jpg'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0.1,
        )
    # qr.add_data('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    qr.add_data(ip+'/'+qr_dir)

    qr_img = qr.make_image(image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer())
    # img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
    qr_s = 140
    qr_img = qr_img.resize((qr_s,qr_s))
    plate.paste(qr_img,(612-int(qr_s/2),3462))
    final = plate.convert("RGB")
    final.save(out_dir)
    return qr_dir



