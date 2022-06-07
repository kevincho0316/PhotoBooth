import win32ui, win32con
from PIL import Image, ImageWin

def print_pic(printer_name,filename):

    try:
        img = Image.open(filename, 'r')
    except:
        print("error")
        return

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    horzres = hdc.GetDeviceCaps(win32con.HORZRES)
    vertres = hdc.GetDeviceCaps(win32con.VERTRES)

    landscape = horzres > vertres

    if landscape:
        if img.size[1] > img.size[0]:
            # print('Landscape mode, tall image, rotate bitmap.')
            img = img.rotate(90, expand=True)
    else:
        if img.size[1] < img.size[0]:
            # print('Portrait mode, wide image, rotate bitmap.')
            img = img.rotate(90, expand=True)

    img_width = img.size[0]
    img_height = img.size[1]

    if landscape:
        #we want image width to match page width
        ratio = vertres / horzres
        max_width = img_width
        max_height = (int)(img_width * ratio)
    else:
        #we want image height to match page height
        ratio = horzres / vertres
        max_height = img_height
        max_width = (int)(max_height * ratio)

    #map image size to page size
    hdc.SetMapMode(win32con.MM_ISOTROPIC)
    hdc.SetViewportExt((horzres, vertres));
    hdc.SetWindowExt((max_width, max_height))

    #offset image so it is centered horizontally
    offset_x = (int)((max_width - img_width)/2)
    offset_y = (int)((max_height - img_height)/2)
    hdc.SetWindowOrg((-offset_x, -offset_y)) 

    hdc.StartDoc('Result')
    hdc.StartPage()

    dib = ImageWin.Dib(img)
    dib.draw(hdc.GetHandleOutput(), (0, 0, img_width, img_height))

    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()

    print('%s-sucess'%(filename))
    # print( 'Debug info:' )
    # print( 'Landscape: %d' % landscape )
    # print( 'horzres: %d' % horzres )
    # print( 'vertres: %d' % vertres )

    # print( 'img_width: %d' % img_width )
    # print( 'img_height: %d' % img_height )

    # print( 'max_width: %d' % max_width )
    # print( 'max_height: %d' % max_height )

    # print( 'offset_x: %d' % offset_x )
    # print( 'offset_y: %d' % offset_y )

