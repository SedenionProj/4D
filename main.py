import pygame
from pygame.locals import *
import numpy as np
from math4D import Math

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit

class Vertex:
    def __init__(self,x,y,z = 1,w = 1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1920, 1080
        self.scale = (7111, 4000)
        self.s = pygame.Surface(self.scale)
        Math.init(self.width,self.height)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        
        self._running = True
        self.cube = [Vertex(-1,-1,-1),Vertex(-1,1,-1),Vertex(1,1,-1),Vertex(1,-1,-1),
                     Vertex(-1,-1, 1),Vertex(-1,1, 1),Vertex(1,1, 1),Vertex(1,-1, 1)]
        
        self.tesseract = [Vertex(-1,-1,-1, -1),Vertex(-1,1,-1, -1),Vertex(1,1,-1, -1),Vertex(1,-1,-1, -1),
                          Vertex(-1,-1, 1, -1),Vertex(-1,1, 1, -1),Vertex(1,1, 1, -1),Vertex(1,-1, 1, -1),
                          Vertex(-1,-1,-1, 1),Vertex(-1,1,-1, 1),Vertex(1,1,-1, 1),Vertex(1,-1,-1, 1),
                          Vertex(-1,-1, 1, 1),Vertex(-1,1, 1, 1),Vertex(1,1, 1, 1),Vertex(1,-1, 1, 1)]
        
        #self.tesseract = []
        #for x in range(5):
        #    for y in range(5):
        #        for z in range(5):
        #            for w in range(5):
        #                if (x/5-0.4)**2*(y/5-0.4)**2-(z/5-0.4)**2*(w/5-0.4)**2<0.3:
        #                    self.tesseract.append(Vertex(x/5-0.4,y/5-0.4,z/5-0.4,w/5-0.4))
        
        self.cam3D = np.array([0.0,0.0,1.0])
        self.cam4D = np.array([0.0,0.0,0.0,3.0])
        self.font = pygame.font.SysFont(None, 18)
        
        self.keys = [pygame.K_z,pygame.K_s,pygame.K_q,pygame.K_d,pygame.K_r,pygame.K_f,
                     pygame.K_LSHIFT,pygame.K_SPACE,pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,
                     pygame.K_RIGHT,pygame.K_p,pygame.K_m,pygame.K_o,pygame.K_l,
                     pygame.K_i,pygame.K_k,pygame.K_u,pygame.K_j,pygame.K_KP5,pygame.K_KP2,
                     pygame.K_KP1,pygame.K_KP3,pygame.K_KP7,pygame.K_KP8,pygame.K_t,pygame.K_g,pygame.K_y,pygame.K_h,pygame.K_b,pygame.K_n]
        self.hold = [0]*len(self.keys)
        self.accel = [0]*len(self.keys)

        self.MAX_ACCEL = 0.07
        self.frame = 0

    def connect(self, p1, p2,col):
        pygame.draw.line(self._display_surf, col, p1, p2)

            
    def draw3D(self):
        vert = []

        for vt in self.cube:
            v = np.array([vt.x,vt.y,vt.z])
            v = Math.Rotation3D_X(v)
            v = Math.Rotation3D_Y(v)
            v = Math.Rotation3D_Z(v)

            v+=self.cam3D

            if v[2]>0:
                vert.append(Math.ToScreenSpace(Math.Projection3D(v)))

        

        for i in range(4):
            try:
                self.connect(vert[i%4],vert[(i+1)%4],(255, 83, 83))
                self.connect(vert[i%4+4],vert[(i+1)%4+4],(255, 83, 83))
                self.connect(vert[i%4],vert[i%4+4],(155,155,255))
            except:
                pass

        for v in vert:
            pygame.draw.circle(self._display_surf, (255,255,255), v[:2], 3)
        

    def draw4D(self):
        vert = []
        for vt in self.tesseract:

            v = np.array([vt.x,vt.y,vt.z,vt.w])
            
            v = Math.Rotation4D_XW(v)
            v = Math.Rotation4D_YW(v)
            v = Math.Rotation4D_ZW(v)

            v = Math.Rotation4D_YZ(v)
            v = Math.Rotation4D_XZ(v)
            v = Math.Rotation4D_XY(v)

            v += self.cam4D

            v = Math.Projection4D(v)

            v = Math.Rotation3D_X(v)
            v = Math.Rotation3D_Y(v)
            v = Math.Rotation3D_Z(v)

            v += self.cam3D

            if v[2]>0:
                v = Math.Projection3D(v)
                vert.append(Math.ToScreenSpace(v))
        
        for i in range(4):
            try:
                self.connect(vert[i%4  ],vert[(i+1)%4  ],(255, 83, 83))
                self.connect(vert[i%4+4],vert[(i+1)%4+4],(255, 83, 83))
                self.connect(vert[i%4  ],vert[i%4+4    ],(255, 83, 83))

                self.connect(vert[i%4   +8],vert[(i+1)%4   +8],(255, 226, 83))
                self.connect(vert[i%4+4 +8],vert[(i+1)%4+4 +8],(255, 226, 83))
                self.connect(vert[i%4   +8],vert[i%4+4     +8],(255, 226, 83))

                self.connect(vert[i%4  ],vert[i%4   +8],(155,155,255))
                self.connect(vert[i%4+4],vert[i%4+4 +8],(155,155,255))
                self.connect(vert[i%4  ],vert[i%4   +8],(155,155,255))
            except:
                pass
           
        for v in vert:
            pygame.draw.circle(self._display_surf, (255,255,255), v[:2], 3)

            
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            for i in range(len(self.keys)):
                if event.key == self.keys[i]:
                    self.hold[i] = True

        if event.type == pygame.KEYUP:
            for i in range(len(self.keys)):
                if event.key == self.keys[i]:
                    self.hold[i] = False
    
    def on_loop(self):
        
        

        self.cam3D -= np.array([0,0,self.accel[0]])
        self.cam3D += np.array([0,0,self.accel[1]])
        self.cam3D += np.array([self.accel[2],0,0])
        self.cam3D -= np.array([self.accel[3],0,0])
        self.cam4D += np.array([0,0,0,self.accel[4]])
        self.cam4D -= np.array([0,0,0,self.accel[5]])
        self.cam3D -= np.array([0,self.accel[6],0])
        self.cam3D += np.array([0,self.accel[7],0])

        Math.rotationXW+=self.accel[8]
        Math.rotationXW-=self.accel[9]
        Math.rotationYW+=self.accel[10]
        Math.rotationYW-=self.accel[11]
        Math.rotationZW-=self.accel[12]
        Math.rotationZW+=self.accel[13]
        Math.rotationXY-=self.accel[14]
        Math.rotationXY+=self.accel[15]
        Math.rotationXZ-=self.accel[16]
        Math.rotationXZ+=self.accel[17]
        Math.rotationYZ-=self.accel[18]
        Math.rotationYZ+=self.accel[19]

        Math.rotationX-=self.accel[20]
        Math.rotationX+=self.accel[21]
        Math.rotationY-=self.accel[22]
        Math.rotationY+=self.accel[23]
        Math.rotationZ-=self.accel[24]
        Math.rotationZ+=self.accel[25]

        self.cam4D += np.array([0,0,self.accel[26],0])
        self.cam4D -= np.array([0,0,self.accel[27],0])
        self.cam4D += np.array([0,self.accel[28],0,0])
        self.cam4D -= np.array([0,self.accel[29],0,0])
        self.cam4D += np.array([self.accel[30],0,0,0])
        self.cam4D -= np.array([self.accel[31],0,0,0])

        for i in range(len(self.keys)):
            if self.hold[i]:
                self.accel[i] +=  0.001
            else:
                self.accel[i] -=  0.001

        for i in range(len(self.accel)):
            if self.accel[i] > self.MAX_ACCEL:
                self.accel[i] = self.MAX_ACCEL
            elif self.accel[i] < 0:
                self.accel[i] = 0

        self.draw4D()
        #self.draw3D()
        
        if True:
            c=255/self.MAX_ACCEL
            self._display_surf.blit(self.font.render("4D rot XW : "+str(round(Math.rotationXW,2)), True, 
                                                     (255-self.accel[8]*c,255-self.accel[9]*c,255-max(self.accel[9],self.accel[8])*c)), (1980//2-290, 1080//2-140))
            self._display_surf.blit(self.font.render("4D rot YW : "+str(round(Math.rotationYW,2)), True, 
                                                     (255-self.accel[10]*c,255-self.accel[11]*c,255-max(self.accel[11],self.accel[10])*c)), (1980//2-290, 1080//2-130))
            self._display_surf.blit(self.font.render("4D rot ZW : "+str(round(Math.rotationZW,2)), True, 
                                                     (255-self.accel[13]*c,255-self.accel[12]*c,255-max(self.accel[12],self.accel[13])*c)), (1980//2-290, 1080//2-120))
            self._display_surf.blit(self.font.render("4D rot XY : "+str(round(Math.rotationXY,2)), True, 
                                                     (255-self.accel[15]*c,255-self.accel[14]*c,255-max(self.accel[14],self.accel[15])*c)), (1980//2-290, 1080//2-110))
            self._display_surf.blit(self.font.render("4D rot XZ : "+str(round(Math.rotationXZ,2)), True, 
                                                     (255-self.accel[17]*c,255-self.accel[16]*c,255-max(self.accel[16],self.accel[17])*c)), (1980//2-290, 1080//2-100))
            self._display_surf.blit(self.font.render("4D rot YZ : "+str(round(Math.rotationYZ,2)), True, 
                                                     (255-self.accel[19]*c,255-self.accel[18]*c,255-max(self.accel[18],self.accel[19])*c)), (1980//2-290, 1080//2-90))

            self._display_surf.blit(self.font.render("3D rot X : "+str(round(Math.rotationX,2)), True, 
                                                     (255-self.accel[21]*c,255-self.accel[20]*c,255-max(self.accel[20],self.accel[21])*c)), (1980//2-290, 1080//2-70))
            self._display_surf.blit(self.font.render("3D rot Y : "+str(round(Math.rotationY,2)), True, 
                                                     (255-self.accel[23]*c,255-self.accel[22]*c,255-max(self.accel[22],self.accel[23])*c)), (1980//2-290, 1080//2-60))
            self._display_surf.blit(self.font.render("3D rot Z : "+str(round(Math.rotationZ,2)), True, 
                                                     (255-self.accel[25]*c,255-self.accel[24]*c,255-max(self.accel[24],self.accel[25])*c)), (1980//2-290, 1080//2-50))

            self._display_surf.blit(self.font.render("4D X : "+str(round(self.cam4D[0],2)), True, 
                                                     (255-self.accel[30]*c,255-self.accel[31]*c,255-max(self.accel[31],self.accel[30])*c)), (1980//2-290, 1080//2-30))
            self._display_surf.blit(self.font.render("4D Y : "+str(round(self.cam4D[1],2)), True, 
                                                     (255-self.accel[28]*c,255-self.accel[29]*c,255-max(self.accel[29],self.accel[28])*c)), (1980//2-290, 1080//2-20))
            self._display_surf.blit(self.font.render("4D Z : "+str(round(self.cam4D[2],2)), True, 
                                                     (255-self.accel[26]*c,255-self.accel[27]*c,255-max(self.accel[27],self.accel[26])*c)), (1980//2-290, 1080//2-10))
            self._display_surf.blit(self.font.render("4D W : "+str(round(self.cam4D[3],2)), True, 
                                                     (255-self.accel[4]*c,255-self.accel[5]*c,255-max(self.accel[5],self.accel[4])*c)), (1980//2-290, 1080//2-0))

            self._display_surf.blit(self.font.render("3D X : "+str(round(self.cam3D[0],2)), True, 
                                                     (255-self.accel[2]*c,255-self.accel[3]*c,255-max(self.accel[3],self.accel[2])*c)), (1980//2-290, 1080//2+20))
            self._display_surf.blit(self.font.render("3D Y : "+str(round(self.cam3D[1],2)), True, 
                                                     (255-self.accel[7]*c,255-self.accel[6]*c,255-max(self.accel[6],self.accel[7])*c)), (1980//2-290, 1080//2+30))
            self._display_surf.blit(self.font.render("3D Z : "+str(round(self.cam3D[2],2)), True, 
                                                     (255-self.accel[1]*c,255-self.accel[0]*c,255-max(self.accel[0],self.accel[1])*c)), (1980//2-290, 1080//2+40))

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        clock = pygame.time.Clock()

        while( self._running ):
            self._display_surf.fill((32, 18, 55))
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            pygame.transform.scale(self._display_surf, self.scale,self.s)
            self._display_surf.blit(self.s, ((-self.scale[0]+self.width)//2, (-self.scale[1]+self.height)//2))
            pygame.display.flip()
            clock.tick(60)

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()