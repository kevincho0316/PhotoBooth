from turtle import back
import cv2
# rgb 이미지 불러오기

#  0 = first page
#  1 = select
#  2
#  3
#  4
#  5
import requests

files = {
    'id': (None, '"1"'),
    'type': (None, '"elon"'),
    'pic1': open('"/elon/backgrounds.png"', 'rb'),
    'pic2': open('"/elon/foregrounds.png"', 'rb'),
    'pic3': open('"/elon/l_2021071602000853400181201-1.jpg"', 'rb'),
    'pic4': open('"/elon/mask.png"', 'rb'),
}

response = requests.post('http://104.197.148.203:5000/predict', files=files)
# state = 0

# back = cv2.imread('client/first.png')
# # rgb 이미지 보기
# while True:
#     cv2.imshow('mainpage', back)
#     cv2.waitKey(0)
#     key = cv2.waitKey()  # 키보드 입력을 무한 대기, 8비트 마스크처리
#     # print(key, chr(key))
#     # 키보드 입력 값,  문자 값 출력
#     if key == ord('q'):         # 'h' 키 이면 좌로 이동
#         if state == 0:
#             back = cv2.imread('client/second.png')
#             state += 1
#         elif state == 1:
#             types = 'elon'
#             back = cv2.imread('client/1.png')
#             state += 1
#     elif key == ord('w'):       # 'j' 키 이면 아래로 이동
#         if state == 0:
#             back = cv2.imread('client/second.png')
#             state += 1
#         elif state == 1:
#             types = 'depth'
#             back = cv2.imread('client/1.png')
#             state += 1
#     elif key == ord('e'):       # 'k' 키 이면 위로 이동
#         if state == 0:
#             back = cv2.imread('client/second.png')
#             state += 1
#         elif state == 1:
#             types = 'arcane'
#             back = cv2.imread('client/1.png')
#             state += 1
#     elif key == ord('t'):
#         print("t")
#         if state == 5:
#             back = cv2.imread('client/process.png')
#             state += 1
#         elif state == 6:
#             state = 0
#             back = cv2.imread('client/first.png')
#         elif state >= 2:
#             back = cv2.imread('client/%d.png' % (state))
#             state += 1
# rgb

# 새로운 좌표로 창 이동
