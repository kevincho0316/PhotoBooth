import cv2
from pygame import SRCALPHA


def elon_sticker(dst_f, ID):
    src = cv2.imread(dst_f, cv2.IMREAD_UNCHANGED)
    if ID == 1:
        dst = cv2.imread('elon/foregrounds.png')
    elif ID == 2:
        src = cv2.imread('elon/foregrounds.png')
    elif ID == 3:
        src = cv2.imread('elon/foregrounds.png')
    elif ID == 4:
        src = cv2.imread('elon/foregrounds.png')

    mask = src[:, :, -1]    # mask는 알파 채널로 만든 마스크 영상
    
    # mask = cv2.imread('elon\mask.png')    # mask는 알파 채널로 만든 마스크 영상
    src = src[:, :, 0:3]    # src는 b, g, r 3채널로 구성된 컬러 영상
    dst = cv2.resize(dst, (1080, 720))

    h, w = src.shape[:2]

    crop = dst[0:h, 0:w]    # src, mask와 같은 크기의 부분 영상 추출

    cv2.copyTo(src, mask, crop)

    # cv2.imshow('src', src)
    # cv2.imshow('dst', dst)
    # cv2.imshow('mask', mask)
    out = 'elon/output/' + dst_f.split('/')[-1].split('.')[0]+'.jpg'
    cv2.imwrite(out, dst)
    return out


dst2 = 'elon/backgrounds.png'

print(elon_sticker(dst2, 1))


# vid = cv2.VideoCapture(0)
# while True:

#     ret, frame = vid.read()
#     cv2.imshow('dope', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break

# vid.release()
# cv2.destroyAllWindows()
