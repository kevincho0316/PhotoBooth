import cv2 
def elon_sticker(src, dst):
    mask = src[:, :, -1]    # mask는 알파 채널로 만든 마스크 영상
    src = src[:, :, 0:3]    # src는 b, g, r 3채널로 구성된 컬러 영상
    dst = cv2.resize(dst, (1080,720))


    h, w = src.shape[:2]

    crop = dst[0:h, 0:w]    # src, mask와 같은 크기의 부분 영상 추출

    cv2.copyTo(src, mask, crop)

    # cv2.imshow('src', src)
    cv2.imshow('dst', dst)
    # cv2.imshow('mask', mask)


src2 = cv2.imread('elon/foregrounds.png', cv2.IMREAD_UNCHANGED)
dst2 = cv2.imread('elon/backgrounds.png', cv2.IMREAD_COLOR)
vid = cv2.VideoCapture(0)
  
while True:

    ret, frame = vid.read()
    elon_sticker(src2, frame)

    if cv2.waitKey(1) == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()