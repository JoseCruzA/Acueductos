import pygame
import sys
import os
import subprocess
import ctypes
from .Cursor import Cursor
from .Boton import Boton

pygame.init()


class GUI:

    def __init__(self, grafo):
        self.grafo = grafo
        self.cursor = Cursor()
        self.pintar()
        self.n = 0

    def screen_size(self):
        self.n = 0
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]), int(line.split()[9][:-1]))
        return size

    def pintar(self):
        if os.name is "posix":
            size = self.screen_size()
            ventana = pygame.display.set_mode(size)
        else:
            ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        pygame.display.set_caption("Grafo")
        fuente = pygame.font.SysFont("Arial Narrow", 30)
        fuenteb = pygame.font.SysFont("Arial Narrow", 25)
        if os.name == "posix":
            icon = pygame.image.load(
                "/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/acueducto.png")
            imagen1 = pygame.image.load(
                "/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/boton.png")
            imagen = pygame.image.load(
                "/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/boton1.png")
            barrio = pygame.image.load(
                "/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/Barrio.png")
            tanque = pygame.image.load(
                "/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/tanque.png")
        else:
            icon = pygame.image.load(
                "I:\\Archivos de la U\\Mi principe\\ProyectoII estructuras\\Acueductos\\Imágenes\\acueducto.png")
            imagen1 = pygame.image.load(
                "I:\\Archivos de la U\\Mi principe\\ProyectoII estructuras\\Acueductos\\Imágenes\\boton.png")
            imagen = pygame.image.load(
                "I:\\Archivos de la U\\Mi principe\\ProyectoII estructuras\\Acueductos\\Imágenes\\boton1.png")
            barrio = pygame.image.load(
                "I:\\Archivos de la U\\Mi principe\\ProyectoII estructuras\\Acueductos\\Imágenes\\Barrio.png")
            tanque = pygame.image.load(
                "I:\\Archivos de la U\\Mi principe\\ProyectoII estructuras\\Acueductos\\Imágenes\\tanque.png")
        icon = pygame.transform.scale(icon, (32, 32))
        pygame.display.set_icon(icon)
        imagen = pygame.transform.scale(imagen, (150, 80))
        imagen1 = pygame.transform.scale(imagen1, (150, 80))
        barrio = pygame.transform.scale(barrio, (100, 100))
        tanque = pygame.transform.scale(tanque, (30, 50))
        #fondo = pygame.image.load("/run/media/josec/Jose Cruz/Documentos/Pycharm Projects/Grafos/Imágenes/fondo.jpeg")
        #fondo = pygame.transform.scale(fondo, size)
        boton = Boton(imagen, imagen1, 50, 50)
        agregar = fuenteb.render("Agregar barrio", True, (0, 0, 0))

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(boton.rect):
                        self.grafo = boton.agregar(self.grafo)
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            ventana.fill((255, 255, 255))
            self.cursor.update()
            boton.update(ventana, self.cursor, agregar)
            if self.grafo is None:
                print("No hay grafo")
                pygame.quit()
                sys.exit()
            else:
                for j in range(0, len(self.grafo.aristas)):
                    if self.grafo.aristas[j].origen.x < self.grafo.aristas[j].destino.x:
                        posx = self.grafo.aristas[j].origen.x + \
                               ((self.grafo.aristas[j].destino.x - self.grafo.aristas[j].origen.x)/2)
                    else:
                        posx = self.grafo.aristas[j].destino.x + \
                               ((self.grafo.aristas[j].origen.x - self.grafo.aristas[j].destino.x)/2)
                    if self.grafo.aristas[j].origen.y < self.grafo.aristas[j].destino.y:
                        posy = self.grafo.aristas[j].origen.y + \
                               ((self.grafo.aristas[j].destino.y - self.grafo.aristas[j].origen.y)/2)
                    else:
                        posy = self.grafo.aristas[j].destino.y + \
                               ((self.grafo.aristas[j].origen.y - self.grafo.aristas[j].destino.y)/2)
                    texto1 = fuente.render(str(self.grafo.aristas[j].peso), True, (0, 0, 0))
                    ventana.blit(texto1, (posx, posy))
                    pygame.draw.line(ventana, self.grafo.aristas[j].color,
                                     (self.grafo.aristas[j].origen.x, self.grafo.aristas[j].origen.y),
                                     (self.grafo.aristas[j].destino.x, self.grafo.aristas[j].destino.y), 2)
                for i in range(len(self.grafo.nodos)):
                    if self.grafo.nodos[i].tanque is True:
                        ventana.blit(tanque, (self.grafo.nodos[i].x + 30, self.grafo.nodos[i].y-55))

                    ventana.blit(barrio, (self.grafo.nodos[i].x-45, self.grafo.nodos[i].y-55))
            pygame.display.update()
