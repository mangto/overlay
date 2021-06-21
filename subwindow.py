import pygame, win32api, win32con, win32gui, os,sys, math, time
from win32api import GetSystemMetrics
from ctypes import windll
import ctypes

def hide_from_taskbar(hw):
    try:
        win32gui.ShowWindow(hw, SW_HIDE)
        win32gui.SetWindowLong(hw, GWL_EXSTYLE,win32gui.GetWindowLong(hw, GWL_EXSTYLE)| WS_EX_TOOLWINDOW)
        win32gui.ShowWindow(hw, SW_SHOW)
    except win32gui.error:
        print("Error while hiding the window")
        return None
class draw:
    def circle(surface, x, y, radius, color):
        global circleF
        surface.blit(pygame.transform.smoothscale(circleF,(radius*2,radius*2)),(x-radius,y-radius))
    def rrect(surface, x, y, sx, sy, radius, color,edge=(1,1,1,1)):
        if sx < radius*2:
            sx = radius*2
        if sy < radius*2:
            sy = radius*2
        pygame.draw.rect(surface,color,[x+radius,y,sx-radius*2,sy])
        pygame.draw.rect(surface,color,[x,y+radius,sx,sy-radius*2])
        pygame.draw.circle(surface,color,(x+radius,y+radius),radius)
        pygame.draw.circle(surface,color,(x+sx-radius,y+radius),radius)
        pygame.draw.circle(surface,color,(x+radius,y+sy-radius),radius)
        pygame.draw.circle(surface,color,(x+sx-radius,y+sy-radius),radius)
    def aarrect(surface, x, y, sx, sy, radius, color,edge=(1,1,1,1)):
        if sx < radius*2:
            sx = radius*2
        if sy < radius*2:
            sy = radius*2
        pygame.draw.rect(surface,color,[x+radius,y,sx-radius*2,sy])
        pygame.draw.rect(surface,color,[x,y+radius,sx,sy-radius*2])
        draw.circle(surface,x+radius,y+radius,radius,color)
        draw.circle(surface,x+sx-radius,y+radius,radius,color)
        draw.circle(surface,x+radius,y+sy-radius,radius,color)
        draw.circle(surface,x+sx-radius,y+sy-radius,radius,color)
start_time = time.time()
pygame.init()
window = pygame.display.set_mode((1,1),pygame.NOFRAME)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(255,0,128)), 255, win32con.LWA_COLORKEY)
###hide_from_taskbar(hwnd)
clock = pygame.time.Clock()
circleF = pygame.image.load('.\\cir.deluF')
pygame.display.set_caption('DELU OVERLAY SHOWBOX')
window = pygame.display.set_mode((120,260),pygame.NOFRAME) #GetSystemMetrics(0),GetSystemMetrics(1))
print('%s' % (time.time()-start_time))
mainhwnd= win32gui.FindWindow(None, "DELU OVERLAY")
visible=True
while True:
    mainrect = win32gui.GetWindowRect(mainhwnd)
    w, h = pygame.display.get_surface().get_size()
    x=mainrect[0]
    y=mainrect[1]
    if mainrect[1] > GetSystemMetrics(1) - h-50:
        y = y- h+50
    windll.user32.MoveWindow(hwnd, x+60, y, w, h, False)
    flags, hcursor, (px,py) = win32gui.GetCursorInfo()
    Mdistance = math.sqrt((x+25-px)**2+(mainrect[1]+25-py)**2)
    window.fill((255,0,128))
    if Mdistance > 35 and pygame.mouse.get_focused() == False:
        visible=False
    if Mdistance < 25:
        visible = True
    if visible== True:
        draw.rrect(window,0,0,120,260,9,(121,121,121))
        draw.aarrect(window,1,1,120-2,260-2,9,(255,255,255))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    