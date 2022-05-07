import time
start = time.time() 
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=10,
    border=0.1,
    )
qr.add_data('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=HorizontalBarsDrawer(
), color_mask=HorizontalGradiantColorMask())
# img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())


img_1.save("some_file3.png")

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
