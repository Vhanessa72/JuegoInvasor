import pygame
import sys
from pygame.locals import *
ancho=900
alto=480
listaEnemigo=[]

class Gatito(pygame.sprite.Sprite):
    "Clase para el  gato"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Agregando imagem
        self.Imagen_Gato = pygame.image.load("Imagen/gatito.jpg")
        self.Reducido= pygame.transform.scale(self.Imagen_Gato, (200,200))
        self.rect = self.Reducido.get_rect()
        self.rect.centerx =ancho/2
        self.rect.centery =alto-80

        self.listaDisparo=[]
        self.Vida=True
        self.velocidad=30

    def movimientoDerecha(self):
        self.rect.right=self.rect.right+self.velocidad
        self.__movimiento()
    def movimientoIzquierda(self):
        self.rect.left=self.rect.left-self.velocidad
        self.__movimiento()
    def __movimiento(self):
        if self.Vida==True:
            if self.rect.left<=0:
                self.rect.left=0
            elif self.rect.right>900:
                self.rect.right=890

    def disparar(self):
        print ("disparo")
    def dibujar(self,superficie):
        superficie.blit(self.Reducido,self.rect)

class Ratones(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagenUno,imagenDos):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA=pygame.image.load(imagenUno)
        self.Reducido_A = pygame.transform.scale(self.imagenA, (80, 100))

        self.imagenB=pygame.image.load(imagenDos)
        self.Reducido_B = pygame.transform.scale(self.imagenB, (80, 100))


        self.listaImagenes=[self.Reducido_A,self.Reducido_B]
        self.posImagen=0
        self.imagenRaton=self.listaImagenes[self.posImagen]
        self.rect = self.imagenRaton.get_rect()


        self.listadisparo=[]
        self.velocidad=20
        self.rect.top=posy
        self.rect.left=posx

        self.derecha=True
        self.contador=0
        self.Max_descenso= self.rect.top+40

        self.limiteDerecha=posx+distancia
        self.limiteIzquierda=posx-distancia

    def comportamiento(self,tiempo):
        self.__movimientos()

    def __movimientos(self):
        if self.contador<3:
            self.__movimientoLateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.Max_descenso== self.rect.top:
            self.contador=0
            self.Max_descenso= self.rect.top+40
        else:
            self.rect.top+=1

    def __movimientoLateral(self):
        if self.derecha==True:
            self.rect.left=self.rect.left+self.velocidad
            if self.rect.left>self.limiteDerecha:
                self.derecha=False
                self.contador+=1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left <self.limiteIzquierda:
                self.derecha=True
    def dibujar(self,superficie):
        superficie.blit(self.imagenRaton,self.rect)

def cargarRatones():
    Ratonc=Ratones(100,110,100,"Imagen/raton1.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(300,80,80,"Imagen/raton2.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(400,30,150,"Imagen/raton1.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(600,48,80,"Imagen/raton2.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(150,10,100,"Imagen/raton1.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(350,129,100,"Imagen/raton2.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(550,160,80,"Imagen/raton1.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)
    Ratonc=Ratones(650,150,200,"Imagen/raton2.jpg","Imagen/raton2.jpg")
    listaEnemigo.append(Ratonc)

def JuegoGato():
     pygame.init()
     ventana=pygame.display.set_mode((ancho,alto))
     pygame.display.set_caption("INVACION")

     ImagenFondo = pygame.image.load("Imagen/fondo.png")
     TamañoCorrecto = pygame.transform.scale(ImagenFondo, (910, 490))

     pygame.mixer.music.load("Imagen/sonido.mp3")
     pygame.mixer.music.play()

     jugador= Gatito()
     cargarRatones()

     enJuego=True
     reloj=pygame.time.Clock()
     tiempo= pygame.time.get_ticks()/1000
     Fuente=pygame.font.SysFont("Italic",30)
     aux=1
     while True:
         Tiempo = pygame.time.get_ticks() / 1000
         if aux==Tiempo:
             aux+=1
         reloj.tick(20)
         #jugador.movimiento()
         for evento in pygame.event.get():
             if evento.type == QUIT:
                 pygame.quit()
                 sys.exit()
             if enJuego==True:
                 if evento.type== pygame.KEYDOWN:
                     if evento.key== K_LEFT:
                         jugador.movimientoIzquierda()
                     elif evento.key== K_RIGHT:
                         jugador.movimientoDerecha()
                     elif evento.key==K_v:
                         jugador.disparar()

         ventana.blit(TamañoCorrecto,(-5,-5))
         #ventana.blit(tiempo, (450,30))

         jugador.dibujar(ventana)

         if len(listaEnemigo)>0:
             for Raton in listaEnemigo:
                 Raton.comportamiento(tiempo)
                 Raton.dibujar(ventana)
                 if Raton.rect.colliderect(jugador.rect):
                     for Raton in listaEnemigo:
                         if Raton.rect.colliderect(jugador.rect):
                             listaEnemigo.remove(Raton)
         Cronometro=Fuente.render("Tiempo: " + str(Tiempo),0,(120,70,0))
         ventana.blit(Cronometro,(400,20))
         pygame.display.update()
JuegoGato()
