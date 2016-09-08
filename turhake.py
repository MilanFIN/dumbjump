#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import * #inputtia varten
import math #putoamisen pyoristusta varten
import sys
pygame.init()
screen = pygame.display.set_mode((640,480))


clock = pygame.time.Clock()


class luoSprite(pygame.sprite.Sprite):
	'''
	luo neliomaisen spriten parametrina annetusta kuvasta
	'''
	def __init__(self,kuvaPolku):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(kuvaPolku).convert()
		self.image = pygame.transform.scale(self.image, (64,64))
		self.rect = self.image.get_rect()

class Peli():
	'''
	koko pelin paaluokka
	'''
	def __init__(self):
		self.__tulevatSpritet = pygame.sprite.Group()
		self.__tulevatValkoiset = pygame.sprite.Group()
		self.__pelaajanSpritet = pygame.sprite.Group()
		#vaihdettavia# vaikuttavat hypyn ominaisuuksiin
		self.__hyppyNopeus = 13
		self.__putoamisKiihtyvyys = 0.5
		#vaihdettavia# yllaolevat siis
		self.__putoamisNopeus = 0
		self.__elossa = True
		self.__pisteet = 0.0
		
		tiedosto = open("./kartat/kartta0.txt", "r")
		rivit = tiedosto.read().splitlines()
		for i in range (len(rivit)):
			merkit = list(rivit[i].strip())
			for j in range(len(merkit)):
				merkki = merkit[j]
				if merkki == ".":
					uusi = luoSprite("./kuvat/tausta.png")
				elif merkki == "#":
					uusi = luoSprite("./kuvat/alusta.png")
					self.__tulevatValkoiset.add(uusi)

				uusi.rect.x = 64*j
				uusi.rect.y = 64*i
				self.__tulevatSpritet.add(uusi)
				
				
		self.__pelaajaSprite = luoSprite("./kuvat/pelaaja.png")
		self.__pelaajaSprite.rect.x = 150
		self.__pelaajaSprite.rect.y = 200
		self.__pelaajanSpritet.add(self.__pelaajaSprite)
		

	def lataaSeuraava(self):
		
		luku = random.randint(1,6)
		tiedosto = open("./kartat/kartta"+str(luku)+".txt", "r")
		rivit = tiedosto.read().splitlines()
		for i in range (len(rivit)):
			merkit = list(rivit[i].strip())
			for j in range(len(merkit)):
				merkki = merkit[j]
				if merkki == ".":
					uusi = luoSprite("./kuvat/tausta.png")
				elif merkki == "#":
					uusi = luoSprite("./kuvat/alusta.png")
					self.__tulevatValkoiset.add(uusi)

				uusi.rect.x = 64*j+640
				uusi.rect.y = 64*i
				self.__tulevatSpritet.add(uusi)
				
				
	def hyppaa(self):
		if not self.__elossa:
			return
		if self.__putoamisNopeus == 0:
			self.__putoamisNopeus = - self.__hyppyNopeus	
	def piirrä(self):
		if not self.__elossa:
			fontti=pygame.font.Font(None,50)
			teksti=fontti.render("Pisteet:"+str(math.ceil(self.__pisteet)), 1,(255,255,0)) #keltainen vari
			screen.blit(teksti, (100, 100))
			teksti2=fontti.render("Enter aloittaa uudestaan",1,(255,255,0)) 
			screen.blit(teksti2, (100, 140))
			teksti3=fontti.render("Välilyönti hyppää",1,(255,255,0)) 
			screen.blit(teksti3, (100, 180))
		else:
			
			self.__tulevatSpritet.draw(screen)
			self.__pelaajanSpritet.draw(screen)
			
			fontti=pygame.font.Font(None,30)
			teksti=fontti.render("Pisteet:"+str(math.ceil(self.__pisteet)), 1,(255,255,0)) #keltainen vari
			screen.blit(teksti, (0, 0))
		
	def siirrä(self):
		if not self.__elossa:
			return
		for i in self.__tulevatSpritet:
			if i.rect.x < -64:#vanhojen poisto
				self.__tulevatSpritet.remove(i)
				if i in self.__tulevatValkoiset:
					self.__tulevatValkoiset.remove(i)
			else:#muiden siirto jos ei tormaysta
				i.rect.x -= 2
				tormays = pygame.sprite.collide_rect(self.__pelaajaSprite, i)
				if tormays == 1:
					if i in self.__tulevatValkoiset:
						self.osuma()
						
		self.__putoamisNopeus += self.__putoamisKiihtyvyys
		self.__pelaajaSprite.rect.y += math.ceil(self.__putoamisNopeus) #ceiling tarpeen, koska siirto ei voi olla desimaaliluku
		for i in self.__tulevatValkoiset:
			tormays = pygame.sprite.collide_rect(self.__pelaajaSprite, i)
			if tormays == 1:
				self.__pelaajaSprite.rect.y -= math.ceil(self.__putoamisNopeus)
				self.__putoamisNopeus = 0
				break
		self.__pisteet += 0.1
		
	def osuma(self):
		
		self.__elossa = False
		pygame.time.delay(1000)
	




def main():
	peli = Peli()
	peli.lataaSeuraava()
	laskuri = 0
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()
			if keys[K_SPACE]:
				peli.hyppaa()
			if keys[K_RETURN]:
				peli.__init__()
				peli.lataaSeuraava()
				laskuri = 0
				
		
		screen.fill((0,0,0))
		peli.piirrä()
		pygame.display.flip()
		peli.siirrä()
		laskuri+=1
		if laskuri == 320:
			peli.lataaSeuraava()
			laskuri = 0
		
		clock.tick(60)


main()
