import pygame, win32api, win32con, win32gui, os,sys, math
from win32api import GetSystemMetrics
from ctypes import windll
import ctypes
from pygame import gfxdraw
from win32con import SWP_NOMOVE 
from win32con import SWP_NOSIZE 
from win32con import SW_HIDE
from win32con import SW_SHOW
from win32con import HWND_TOPMOST
from win32con import GWL_EXSTYLE 
from win32con import WS_EX_TOOLWINDOW
import win32gui, win32con
import keyboard


pygame.init()

winW, winH  = 50,50
rw, rh = winW,winH
winposx = -20
winposy = (GetSystemMetrics(1)-winH)/2-80
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winposx,winposy)
window = pygame.display.set_mode([1,1],pygame.NOFRAME)
pygame.display.set_caption("GICON OVERLAY")
clock = pygame.time.Clock()
fps = 60
state_left = win32api.GetKeyState(0x01)
state_right = win32api.GetKeyState(0x02)
state_middle = win32api.GetKeyState(0x04)

basecolor = (20,20,20)
tfcolor = (255,0,128)

dx, dy=0, 0
clicking = False
moving = False
lclick = False
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(255,0,128)), 255, win32con.LWA_COLORKEY)
hwnd = win32gui.FindWindow(None, "GICON OVERLAY")
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

def hide_from_taskbar(hw):
    try:
        win32gui.ShowWindow(hw, SW_HIDE)
        win32gui.SetWindowLong(hw, GWL_EXSTYLE,win32gui.GetWindowLong(hw, GWL_EXSTYLE)| WS_EX_TOOLWINDOW)
        win32gui.ShowWindow(hw, SW_SHOW)
    except win32gui.error:
        print("Error while hiding the window")
        return None

#1은 내려가는거 2는 올라가는거
lastleft1 = 0
lastleft2 = 0
lastright2 = 0
lastright1 = 0
lastmiddle1 = 0
class mouse:
    def middlebtdown():
        global lastmiddle1
        middle = win32api.GetKeyState(0x04)
        if int(lastmiddle1) >=0 and middle <0:
            lastmiddle1 = middle
            return True
        else:
            lastmiddle1 = middle
            return False
    def rightbtdown():
        global lastright1
        right = win32api.GetKeyState(0x02)
        if int(lastright1) >= 0 and right <0:
            lastright1 = right
            return True
        else:
            lastright1=right
            return False
    def rightbtup():
        global lastright2
        right = win32api.GetKeyState(0x02)
        if int(lastright2) < 0 and right >=0:
            lastright2 = right
            return True
        else:
            lastright2=right
            return False
    def leftbtdown():
        global lastleft1
        left = win32api.GetKeyState(0x01)
        if int(lastleft1) >=0 and left <0:
            lastleft1 = left
            return True
        else:
            lastleft1 = left
            return False
    def leftbtup():
        global lastleft2
        left = win32api.GetKeyState(0x01)
        if int(lastleft2) < 0 and left >= 0:
            lastleft2 = left
            return True
        
        else:
            lastleft2 = left
            return False
nowcursor=pygame.SYSTEM_CURSOR_ARROW
class gui:
    def draw():
        global guilist, moving,nowcursor,chc
        chc = False
        for gui_ in guilist:
            gui_.draw()
            mx,my=pygame.mouse.get_pos()
            if mx >=gui_.x and mx <= gui_.x+gui_.sx and my >= gui_.y and my<=gui_.y+gui_.sy:
                if gui_.mouse != pygame.SYSTEM_CURSOR_ARROW and nowcursor != gui_.mouse:
                    if chc == False:
                        if gui_.visible==True:
                            pygame.mouse.set_system_cursor(gui_.mouse)
                            chc=True
        if chc == False:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    class sbutton:
        def __init__(self,x,y,sx,sy,basecolor,onbtcolor,activecolor,edgecolor=(0,0,0),edge=0,text=None,font=None,textcolor=(255,255,255),image=None,on=False,tag=None,images=None,canpress=True,visible=True,switch=True,onbtimage=None,hand=True):
            guilist.append(self)
            self.x=x
            self.y=y
            self.rx=x
            self.ry=y
            self.sx=sx
            self.sy=sy
            self.basecolor=basecolor
            self.onbtcolor=onbtcolor
            self.activecolor=activecolor
            self.edgecolor=edgecolor
            self.edge=edge
            self.text=text
            self.textcolor=textcolor
            self.font =font
            self.image=image
            self.defaultimage=image
            self.on = on
            self.tag=tag
            self.guitype = "sbutton"
            self.images =images
            self.visible=visible
            self.canpress = canpress
            self.switch = switch
            self.onbtimage=onbtimage
            self.mouse=pygame.SYSTEM_CURSOR_HAND
            if hand == False:
                self.mouse=pygame.SYSTEM_CURSOR_ARROW
        def draw(self):
            global leftclick
            left = win32api.GetKeyState(0x01)
            right = win32api.GetKeyState(0x02)
            mx,my= pygame.mouse.get_pos()
            if left < 0:
                leftclick = True
            if mouse.leftbtup() == True:
                leftclick = False
            if self.onbtimage != None:
                if mx >=self.x and mx <= self.x+self.sx and my >= self.y and my<=self.y+self.sy and pygame.mouse.get_focused()==True and left<0:
                    self.image=self.onbtimage
                else:
                    self.image=self.defaultimage
            if self.canpress == True:
                if mx >=self.x and mx <= self.x+self.sx and my >= self.y and my<=self.y+self.sy and pygame.mouse.get_focused()==True:
                    if self.switch == False:
                        if self.on == True:
                            self.on = False
                    color = self.onbtcolor
                else:
                    color = self.basecolor
                if self.on == True:
                    color = self.activecolor
            else:
                color = self.basecolor
            if self.switch == False:
                if mx >=self.x and mx <= self.x+self.sx and my >= self.y and my<=self.y+self.sy and pygame.mouse.get_focused()==True:
                    if left <0:
                        color = self.activecolor
            if self.visible == True:
                if self.edge > 0:
                    pygame.draw.rect(window,self.edgecolor,[self.x,self.y,self.sx,self.sy])
                    pygame.draw.rect(window,color,[self.x+self.edge,self.y+self.edge,self.sx-2*self.edge,self.sy-2*self.edge])
                else:
                    pygame.draw.rect(window,color,[self.x,self.y,self.sx,self.sy])
                if self.image != None:
                    size = self.image.get_rect().size
                    if self.images == None:
                        self.images = size
                    pos = ((self.x+self.sx/2)-self.images[0]/2,(self.y+self.sy/2)-self.images[1]/2)
                    window.blit(self.image,pos)
                if self.text != None:
                    if self.font != None:
                        draw.text(self.text,self.font,window,int(self.x+self.sx/2),int(self.y+self.sy/2),color=self.textcolor)
class draw:
    def text(text, font, window, x, y, cenleft="center", color=(0,0,0)):
        text_obj = font.render(text, True, color)
        text_rect=text_obj.get_rect()
        if(cenleft == "center"):
            text_rect.centerx = x
            text_rect.centery = y
        elif(cenleft == "left"):
            text_rect.left=x
            text_rect.top=y
        elif(cenleft == "right"):
            text_rect.right=x
            text_rect.top=y
        elif(cenleft == "cenleft"):
            text_rect.left=x
            text_rect.centery=y
        elif(cenleft == "cenright"):
            text_rect.right=x
            text_rect.centery=y
        window.blit(text_obj, text_rect)
    def gettsize(text,font):
        return font.render(text,True,(0,0,0)).get_rect().size
    def trirect(surface,x,y,sx,sy,tri,color,edge=(1,1,1,1)):
        if sx < tri*2:
            sx = tri*2
        if sy < tri*2:
            sy = tri*2
        pygame.draw.rect(surface,color,[x+tri,y,sx-tri*2,sy])
        pygame.draw.rect(surface,color,[x,y+tri,sx,sy-tri*2])
        if edge[0] == 1:
            pygame.draw.polygon(surface,color,[[x,y+tri],[x+tri,y],[x+tri,y+tri]])
        else:
            pygame.draw.rect(surface,color,[x,y,tri,tri])
        if edge[1] == 1:
            pygame.draw.polygon(surface,color,[[x+sx-tri,y+1],[x+sx-1,y+tri],[x+sx-tri,y+tri]])
        else:
            pygame.draw.rect(surface,color,[x+sx-tri,y,tri,tri])
        if edge[2] == 1:
            pygame.draw.polygon(surface,color,[[x,y+sy-tri],[x+tri-1,y+sy-1],[x+tri,y+sy-tri]])
        else:
            pygame.draw.rect(surface,color,[x,y+sy-tri,tri,tri])
        if edge[3] == 1:
            pygame.draw.polygon(surface,color,[[x+sx-1,y+sy-tri],[x+sx-tri,y+sy-1],[x+sx-tri,y+sy-tri]])
        else:
            pygame.draw.rect(surface,color,[x+sx-tri,y+sy-tri,tri,tri])
def moveWin():
    global moving, dx, dy, lclick, guilist, winposx,winposy, move, pos, posx, mx,my
    if pygame.mouse.get_focused()==True and pygame.mouse.get_pressed()[0] == 1:
        moving = True
    flags, hcursor, (px,py) = win32gui.GetCursorInfo()
    mx = px - winposx
    my = py - winposy
    left = win32api.GetKeyState(0x01)
    right = win32api.GetKeyState(0x02)
    if moving == True:
        move =True
        mx, my = pygame.mouse.get_pos()
        if move  == True and left<0:
            global mdistancex, mdistancey
            flags, hcursor, (px,py) = win32gui.GetCursorInfo()
            x, y = (px-dx, py-dy)
            winposx = x
            winposy = y
            hwnd = pygame.display.get_wm_info()['window']
            w, h = pygame.display.get_surface().get_size()
            if x < GetSystemMetrics(0)/8:
                pos='left'
                posx=-20
            elif x > GetSystemMetrics(0)/8*7:
                pos='right'
                posx=GetSystemMetrics(0)-30
            if y < GetSystemMetrics(1)-50 and y > 0 and ( pos == 'left' or pos == 'right'):
                    windll.user32.MoveWindow(hwnd, posx, y, w, h, False) #-25 -> x : every where
    if left >= 0:
        moving = False
        move = False
move = False
pos = 'left' # left or right
posx=-20
window = pygame.display.set_mode([winW,winH],pygame.NOFRAME)
hide_from_taskbar(hwnd)
working = True
mainimage = pygame.transform.smoothscale(pygame.image.load('logo.deluF'),(48,48))
guilist = []
mx,my=0,0
Mdistance = 0

class system:
    def display():
        global selectorsize,selector,selectorsize
        window.fill(tfcolor)
        pygame.draw.circle(window,(120,120,120),(25,25),25)
        window.blit(mainimage,(1,1))
        gui.draw()

        pygame.display.update()
    def control():
        global fps
        clock.tick(fps)
    def event():
        global dx,dy, working, selector,selectorsize, winposx,winposy,move, Mdistance, mainimage, pos ,posx
        flags, hcursor, (px,py) = win32gui.GetCursorInfo()
        Mdistance = math.sqrt((winposx+25-px)**2+(winposy+25-py)**2)
        mx = px - winposx
        my = py - winposy
        moveWin()
        posX, posY, width, height = win32gui.GetWindowPlacement(hwnd)[4]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, posX,posY, 0,0, win32con.SWP_NOSIZE)
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("e") == True and keyboard.is_pressed("t") == True and keyboard.is_pressed("p") == True: #escape this page
            working = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:
                    dx, dy = pygame.mouse.get_pos()
while working:
    system.control()
    system.event()
    system.display()
pygame.quit()
sys.exit()
