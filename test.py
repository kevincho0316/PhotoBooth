import cv2

# 마스크 영상을 이용한 영상 합성
src = cv2.imread('elon/foregrounds.png', cv2.IMREAD_COLOR)        # 컬러 영상
mask = cv2.imread('elon/mask.png', cv2.IMREAD_COLOR)  
dst = cv2.imread('elon/backgrounds.png', cv2.IMREAD_COLOR)

# # 파일이 불러오기 확인
# if src is None or mask is None or dst is None:
#     print('Image load failed')
#     sys.exit()


# dst를 꼭 입력값으로 넣어줘야 합니다.
# src, mask, dst크기가 같아야 합니다.
# src, dst 크기가 다르다면 dst 영상을 추출하여 입력값으로 넣어주면 됩니다. (추출한 부분에 scr 형성)
cv2.copyTo(src, mask, dst)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.imshow('mask', mask)
cv2.waitKey()
cv2.destroyAllWindows()