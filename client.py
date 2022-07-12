
from re import template
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
import final_stitch
import printer
from PIL import Image
import ctypes



# py_serial = serial.Serial(
    
#     # Window
#     port='COM4',
    
#     # 보드 레이트 (통신 속도)
#     baudrate=9600,
# )


black = False ########################################컬러 떨어질 경우###############


data_list=[ ['depth/img/doge_mountain/background.png',600,0,(277, 70),'depth/img/doge_mountain/foreground.png'],
            ['depth/img/light_travel/background.png',450,0,(330, 100),'depth/img/light_travel/foreground.png'],
            ['depth/img/radioactive_pool/background.png',500,0,(190, 189),'depth/img/radioactive_pool/foreground.png'],
            ['depth/img/to_the_moon/background.png',450,-15,(320, 35),'depth/img/to_the_moon/foreground.png'],
            ]

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def place(ori_img,mask_fd, id,mode):
    if mode ==1:
        mask = Image.open(mask_fd)
        ori_img = Image.open(ori_img)
    else:
        mask = mask_fd

        

    foreground = Image.open(data_list[id-1][4])
    background = Image.open(data_list[id-1][0])
    
    mask.thumbnail((data_list[id-1][1],data_list[id-1][1])) #한변의 최대 길이
    fw, fh = mask.size
    mask = mask.rotate(data_list[id-1][2],expand=True)

    ori_img.thumbnail((data_list[id-1][1],data_list[id-1][1]))
    fw, fh = ori_img.size
    ori_img = ori_img.rotate(data_list[id-1][2],expand=True)
    


    
    

    background.paste(ori_img,data_list[id-1][3],mask)
    background.paste(foreground,(0,0),foreground)
    # print(m)
    if mode == 0:
        return pilImageToSurface(background)
    elif mode == 1:
        createFolder(B_path +'/depth/output/'+mask_fd.split('/')[-2])
        out_dir = B_path +'/depth/output/'+mask_fd.split('/')[-2]+'/'+mask_fd.split('/')[-1].split('.')[0]+'.jpg'

        background = background.convert("RGB")
        background.save(out_dir)
        return out_dir



def Delete(id):
    os.remove('%d.zip' % (id))
    # os.remove("desk/%d.jpg"% (id))
    
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
    return img
    
def zip(id):
    zip_file = zipfile.ZipFile('%d.zip' % (id), "w")  # "w": write 모드
    for i in range(4):
        zip_file.write(str(i+1)+'.png', compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()
    
def api(id,type,temp,file_dir):
    
    # print(type)
    files = {
        'id': (None, id),
        'type': (None, type),
        'temp': (None, temp),
        'zip': open('%d.zip' % (id), 'rb'),
        
        # 'zip': open('%d.zip' % (id), 'rb'),
    }
    print('[id:%d type:%s temp:%s]'%(id,types,temp))
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
os.environ['SDL_VIDEO_CENTERED'] = '0' #frequency, size, channels, buffersize
pygame.init()
pygame.mixer.init()
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
api_b = False
escape = False
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

    # if py_serial.readable():
        
    #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    #     response = py_serial.readline()
    #     if response != b'\r\n':
    #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    #         # print(response[:len(response)-1].decode())
    #         key = response[:len(response)-1].decode()[0]
    # else:
    #     key = ''              



    # print(state)

    # 키보드 입력 값,  문자 값 출력
    if key == 'q' :         # 'h' 키 이면 좌로 이동
        if state == 0:
            print("_____________________________________")
            # print("[%d]"%id)
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            key = ''
            while True:  
                # if py_serial.readable():
        
                #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
                #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                #     response = py_serial.readline()
                #     if response != b'\r\n':
                #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                #         print(response[:len(response)-1].decode())
                #         key = response[:len(response)-1].decode()[0]
                # else:
                #     key = ''   
                if escape==True:
                    escape=False
                    break    
                
              
                screen.fill((255, 255, 255))
                screen.blit(pygame.image.load('client/elon choose.png'),((win_x/2-540),(win_y/2)-405))
                      
                pygame.display.update()
                if key == 'q':
                    types = 'elon'
                    break
                elif key == 'w':
                    types = 'rupi'
                    break
                elif key == 'e':
                    types = 'meme'
                    break
                for event in pygame.event.get():                
                    if event.type == pygame.KEYDOWN:
                        if event.key==K_q:
                            key = 'q'
                        elif event.key==K_w:
                            key = 'w'
                        elif event.key==K_e:
                            key = 'e'
                        elif event.key==K_z:
                            state = 0
                            back = pygame.image.load('client/first.png')
                            
                            print("__________ESCAPE___________")
                            escape=True
                            break
            
            back = pygame.image.load('client/%s.png'%('elon'))
            state += 2
        elif state == 2:
            types = 'anime'
            back = pygame.image.load('client/%s.png'%(types))
            state += 1
    elif key == 'w':       # 'j' 키 이면 아래로 이동
        if state == 0:
            print("_____________________________________")
            # print("[%d]"%id)
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            key = ''
            while True:  
                # if py_serial.readable():
        
                #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
                #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                #     response = py_serial.readline()
                #     if response != b'\r\n':
                #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                #         print(response[:len(response)-1].decode())
                #         key = response[:len(response)-1].decode()[0]
                # else:
                #     key = ''   
                if escape==True:
                    escape=False
                    break    
                
              
                screen.fill((255, 255, 255))
                screen.blit(pygame.image.load('client/depth choose.png'),((win_x/2-540),(win_y/2)-405))
                      
                pygame.display.update()
                if key == 'q':
                    types = 'depth-elon'
                    break
                elif key == 'w':
                    types = 'depth-flower'
                    break
                elif key == 'e':
                    types = 'depth-pop'
                    break
                for event in pygame.event.get():                
                    if event.type == pygame.KEYDOWN:
                        if event.key==K_q:
                            key = 'q'
                        elif event.key==K_w:
                            key = 'w'
                        elif event.key==K_e:
                            key = 'e'
                        elif event.key==K_z:
                            state = 0
                            back = pygame.image.load('client/first.png')
                            
                            print("__________ESCAPE___________")
                            escape=True
                            break
            
            back = pygame.image.load('client/%s.png'%('depth'))
            state += 2
    elif key == 'e':       # 'k' 키 이면 위로 이동
        if state == 0:
            print("_____________________________________")
            # print("[%d]"%id)
            back = pygame.image.load('client/second.png')
            state += 1
        elif state == 1:
            back = pygame.image.load('client/cartoon choose.png')
            state += 1
        elif state == 2:
            types = 'arcane'
            back = pygame.image.load('client/%s.png'%(types))
            state += 1
            
    elif key == 't' or t_pass == True:
        t_pass = False
        if state == 7:
            key = ''
            view_state=1
            while True:  
                # if py_serial.readable():
        
                #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
                #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                #     response = py_serial.readline()
                #     if response != b'\r\n':
                #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                #         print(response[:len(response)-1].decode())
                #         key = response[:len(response)-1].decode()[0]
                # else:
                #     key = ''   
                if escape==True:
                    escape=False
                    break    
                
              
                screen.fill((255, 255, 255))
                screen.blit(pygame.image.load('client/temp-%d.png' % (view_state)),((win_x/2-540),(win_y/2)-405))
                      
                pygame.display.update()
                if key == 'w':
                    key = ''
                    
                    state = 8
                elif key == 'q':
                    key = ''
                    if view_state != 5:
                        view_state += 1
                elif key == 'e':
                    key = ''
                    if view_state != 1:
                        view_state -= 1
                if state == 8:
                    template_n = view_state
                    break
                    
                    
                    

                for event in pygame.event.get():                
                    if event.type == pygame.KEYDOWN:
                        if event.key==K_q:
                            key = 'q'
                        elif event.key==K_w:
                            key = 'w'
                        elif event.key==K_e:
                            key = 'e'
                        elif event.key==K_z:
                            state = 0
                            back = pygame.image.load('client/first.png')
                            
                            print("__________ESCAPE___________")
                            escape=True
                            break
                    if event.type == pygame.QUIT:                        
                        sys.exit()
        if state == 8:
            api_b = True
            fileout_name=merge(api(int(id), types,template_n, 'desk/'))
            # fileout_name=api(int(id), types, 'desk/')
            back = pygame.image.load('client/process.png')
            printer.print_pic('LG LIP2250', fileout_name,black)           #프린터 설정
            state += 1
        elif state == 9:
            state = 0
            Delete(id)
            back = pygame.image.load('client/first.png')
            print("___________________________")
            api_b = False
            
            id +=1
        elif state >= 3:
            key = ''
            while True:    
                # if py_serial.readable():
        
                #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
                #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                #     response = py_serial.readline()
                #     if response != b'\r\n':
                #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                #         print(response[:len(response)-1].decode())
                #         key = response[:len(response)-1].decode()[0]
                # else:
                #     key = '' 

                if escape==True:
                    escape=False
                    break    
                image = cam.get_image()        
                new_image = pygame.transform.flip(image, True, False)

                pil_string_image = pygame.image.tostring(new_image,"RGBA",False)
                img = Image.frombytes("RGBA",(web_x,web_y),pil_string_image)
                img = final_stitch.crop(img)
                
                if types == 'elon' or types == 'rupi' or types == 'meme':
                    new_image = elon_filter.process(img, (state-3), 0,types)
                elif types == 'depth-elon' or types == 'depth-flower' or types == 'depth-pop':
                    new_image = place(img, img, state-3, 0,types)
                else:
                    new_image=pilImageToSurface(img)
                
                screen.fill((255, 255, 255))
                screen.blit(new_image,((win_x/2-540),(win_y/2)-405))        
                screen.blit(pygame.image.load('client/%d.png' % (state-2)),((win_x/2-540),(win_y/2)-405))
                pygame.display.flip()        
                pygame.display.update()
                if key == 't':
                    key = ''
                    # s= pygame.mixer.Sound("capture.mp3")
                    # pygame.mixer.play()
                    
                    screen.fill((255, 255, 255))
                    screen.blit(new_image,((win_x/2-540),(win_y/2)-405))
                    pygame.display.update()
                    pygame.time.wait(412)
                    image = pygame.transform.flip(image, True, False)
                    pil_string_image_n = pygame.image.tostring(image,"RGBA",False)
                    img2 = Image.frombytes("RGBA",(web_x,web_y),pil_string_image_n)
                    img2 = final_stitch.crop(img2)
                    img2.save('%d.png' % (state-2))
                    state += 1
                    if state == 7:
                        t_pass=True
                        back = pygame.image.load('client/zipping.png')
                        screen.fill((255, 255, 255))
                        screen.blit(back, ((win_x/2-540),(win_y/2)-405)) # 배경 그리기(background 가 표시되는 위치)
                        pygame.display.update()
                        zip(id)
                        back = pygame.image.load('client/loading.png')
                        
                        break

                for event in pygame.event.get():                
                    if event.type == pygame.KEYDOWN:
                        if event.key==K_t:
                            key = 't'
                        elif event.key==K_z:
                            state = 0
                            back = pygame.image.load('client/first.png')
                            
                            print("__________ESCAPE___________")
                            escape=True
                            break
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
            elif event.key==K_z:
                state = 0
                back = pygame.image.load('client/first.png')
                
                print("__________ESCAPE___________")
            elif event.key==K_f:  # f 키를 눌렀을 때
                user32 = ctypes.windll.user32
                screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
                surface = pygame.display.set_mode(screensize, FULLSCREEN)  # 전체화면으로 전환

        if event.type == pygame.QUIT:
            pygame.quit() 
            exit(0)


    screen.fill((255, 255, 255))
    infoObject = pygame.display.Info()
    (win_x,win_y)=(infoObject.current_w, infoObject.current_h)
    screen.blit(back, ((win_x/2-540),(win_y/2)-405)) # 배경 그리기(background 가 표시되는 위치)
    pygame.display.update()


# rgb

# 새로운 좌표로 창 이동
