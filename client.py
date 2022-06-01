
import requests
import pygame ,sys
import pygame.camera
from pygame.locals import *
import os
import serial
import time

py_serial = serial.Serial(
    
    # Window
    port='COM3',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)

def api(id,type,file_dir):
    files = {
        'id': (None, id),
        'type': (None, type),
        'zip': open(file_dir, 'rb'),
    }

    response = requests.post('http://104.197.148.203:5000/predict', files=files)
    return response



clock = pygame.time.Clock()

pos_x = 400
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((1080,810))
pygame.display.set_caption("Dalso Game")
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(640,480))
cam.start()

# while 1:        
#     image = cam.get_image()        
#     new_image = pygame.transform.flip(image, True, False)
#     screen.blit(new_image,(0,0))        
#     pygame.display.flip()        
#     pygame.display.update()

#     for event in pygame.event.get():                
#         if event.type == pygame.QUIT:                        
#             sys.exit()



state = 0

back = pygame.image.load('client/first.png')
# rgb 이미지 보기
while True:
    clock.tick(60)
    screen.blit(back, (0, 0)) # 배경 그리기(background 가 표시되는 위치)
    pygame.display.update()

    commend = input('아두이노에게 내릴 명령:')
    
    py_serial.write(commend.encode())

    
    if py_serial.readable():
        
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
        key = response[:len(response)-1].decode()[0]
    else:
        key = ''              
                
    # 키보드 입력 값,  문자 값 출력
    if key == 'q':         # 'h' 키 이면 좌로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'elon'
            back = pygame.image.load('client/1.png')
            state += 1
    elif key == 'w':       # 'j' 키 이면 아래로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'depth'
            back = pygame.image.load('client/1.png')
            state += 1
    elif key == 'e':       # 'k' 키 이면 위로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'arcane'
            back = pygame.image.load('client/1.png')
            state += 1
    elif key == 't':
        if state == 5:
            back = pygame.image.load('client/process.png')
            state += 1
        elif state == 6:
            state = 0
            back = pygame.image.load('client/first.png')
        elif state >= 2:
            back = pygame.image.load('client/%d.png' % (state))
            state += 1


# rgb

# 새로운 좌표로 창 이동
