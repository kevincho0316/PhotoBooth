
import requests
import urllib.request
import pygame ,sys
import pygame.camera
from pygame.locals import *
import os
import serial
import time
import zipfile
import elon_filter
import depth_filter
import final_stitch
from PIL import Image
import ctypes

# py_serial = serial.Serial(
    
#     # Window
#     port='COM3',
    
#     # 보드 레이트 (통신 속도)
#     baudrate=9600,
# )
def Delete(id):
    os.remove('%d.zip' % (id))
    os.remove("desk/%d.jpg"% (id))
    
    for i in range(4):
        os.remove('%d.png' % (i+1))
    
def merge(img):
    image1 = Image.open(img)
    image2 = Image.open(img)
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0],0))
    new_image.save(img)
    

def api(id,type,file_dir):
    zip_file = zipfile.ZipFile('%d.zip' % (id), "w")  # "w": write 모드
    for i in range(4):
        zip_file.write(str(i+1)+'.png', compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()
    
    
    files = {
        'id': (None, id),
        'type': (None, type),
        'zip': open('%d.zip' % (id), 'rb'),
        
        # 'zip': open('%d.zip' % (id), 'rb'),
    }
    print(files)
    response = requests.post('http://metash.p-e.kr:5000/predict', files=files)

    print(str(response.status_code) + " | " + response.text)
    j=response.json()
    url = j['file']
    print(url)
    urllib.request.urlretrieve(url, "desk/%d.jpg"% (id))
    return "desk/%d.jpg"% (id)





def cam():
    image = cam.get_image()        
    new_image = pygame.transform.flip(image, True, False)
    screen.fill((255, 255, 255))
    screen.blit(new_image,((win_x/2-540),(win_y/2)-405))        
    



clock = pygame.time.Clock()

pos_x = 400
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.init()
pygame.camera.init()

win_x=1280
win_y=1080     #1080임 그 직사각형 모니터
win_iy=824
web_x=1280
web_y=720
screen = pygame.display.set_mode((win_x,win_iy))
pygame.display.set_caption("Dalso Game")
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(web_x,web_y))
cam.start()

key = ''
t_pass = False
state = 0
id = 0

# while 1:        
#     image = cam.get_image()        
#     new_image = pygame.transform.flip(image, True, False)
#     screen.blit(new_image,((win_x/2-540),(win_y/2)-405))        
#     pygame.display.flip()        
#     pygame.display.update()

#     for event in pygame.event.get():                
#         if event.type == pygame.QUIT:                        
#             sys.exit()




back = pygame.image.load('client/first.png')



# rgb 이미지 보기
while True:
    if not os.path.exists('desk/'):
        os.makedirs('desk/')
    clock.tick(60)


    # commend = ('k')
    
    # py_serial.write(commend.encode())

    
    # if py_serial.readable():
        
    #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    #     response = py_serial.readline()
        
    #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    #     print(response[:len(response)-1].decode())
    #     key = response[:len(response)-1].decode()[0]
    # else:
    #     key = ''              







    # 키보드 입력 값,  문자 값 출력
    if key == 'q':         # 'h' 키 이면 좌로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'elon'
            back = pygame.image.load('client/%s.png'%(types))
            state += 1
    elif key == 'w':       # 'j' 키 이면 아래로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'depth'
            back = pygame.image.load('client/%s.png'%(types))
            state += 1
    elif key == 'e':       # 'k' 키 이면 위로 이동
        if state == 0:
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            types = 'arcane'
            back = pygame.image.load('client/%s.png'%(types))
            state += 1
   
    elif key == 't' or t_pass == True:
        t_pass = False
        if state == 6:
            
            merge(api(id, types, 'desk/'))
            
            back = pygame.image.load('client/process.png')
            # print
            state += 1
        elif state == 7:
            state = 0
            
            Delete(id)
            back = pygame.image.load('client/first.png')
            
            id +=1
        elif state >= 2:
            key = ''
            while True:        
                image = cam.get_image()        
                new_image = pygame.transform.flip(image, True, False)
                
                if types == 'elon':
                    pil_string_image = pygame.image.tostring(new_image,"RGBA",False)
                    img = Image.frombytes("RGBA",(web_x,web_y),pil_string_image)
                    img = final_stitch.crop(img)
                    # print(img.size)
                    new_image = elon_filter.process(img, (state-2), 0)
                elif types == 'depth':
                    pil_string_image = pygame.image.tostring(new_image,"RGBA",False)
                    img = Image.frombytes("RGBA",(web_x,web_y),pil_string_image)
                    img = final_stitch.crop(img)
                    new_image = depth_filter.place(img, img, state-2, 0)
                
                
                screen.fill((255, 255, 255))
                screen.blit(new_image,((win_x/2-540),(win_y/2)-405))        
                screen.blit(pygame.image.load('client/%d.png' % (state-1)),((win_x/2-540),(win_y/2)-405))
                pygame.display.flip()        
                pygame.display.update()
                if key == 't':
                    key = ''
                    image = pygame.transform.flip(image, True, False)
                    pil_string_image_n = pygame.image.tostring(image,"RGBA",False)
                    img2 = Image.frombytes("RGBA",(web_x,web_y),pil_string_image_n)
                    img2 = final_stitch.crop(img2)
                    img2.save('%d.png' % (state-1))
                    state += 1
                    if state == 6:
                        t_pass=True
                        back = pygame.image.load('client/loading.png')
                        break

                for event in pygame.event.get():                
                    if event.type == pygame.KEYDOWN:
                        if event.key==K_t:
                            key = 't'
                    if event.type == pygame.QUIT:                        
                        sys.exit()

    

    key = ''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==K_q:
                key = 'q'
            elif event.key==K_w:
                key = 'w'
            elif event.key==K_e:
                key = 'e'
            elif event.key==K_t:
                key = 't'
            elif event.key ==K_f:  # f 키를 눌렀을 때
                user32 = ctypes.windll.user32
                screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
                surface = pygame.display.set_mode(screensize, FULLSCREEN)  # 전체화면으로 전환

        if event.type == pygame.QUIT:
            pygame.quit() 
            exit(0)
    screen.fill((255, 255, 255))
    screen.blit(back, ((win_x/2-540),(win_y/2)-405)) # 배경 그리기(background 가 표시되는 위치)
    pygame.display.update()


# rgb

# 새로운 좌표로 창 이동
