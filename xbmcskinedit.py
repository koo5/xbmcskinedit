#!/usr/bin/python

import xmltodict
#https://github.com/martinblech/xmltodict
#pip install xmltodict

import sys
from random import random

import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((1280, 720))



ks = ["posx", "posy", "width", "height"]




def pk(k,i,l):
	if k in i:
		sys.stdout.write( " " * (l+1) )
		print k+": " + i[k]


def allthere(i, k):
	return len([key for key in k if key in i]) == len(k)
#	found = 0
#	for K in k:
#		if K in i:
#			found = found + 1
#	return found == len(k)


def y(x,l,parpos):

	for i in x:

		sys.stdout.write( " " * l )
		print i["@type"]


#		print i


		for k in ks:
			pk(k, i, l)

		if allthere(i, ks):
			sys.stdout.write( " " * (l+1) )
			print "ALL"

		p = pos(i, parpos)
		rects[p[0]] = i["@type"]

		if i["@type"] == "group":
			y(i["control"], 2, p[0])

def pos(tags,parpos):
	if "posx" in tags:
		if tags["posx"][-1] == 'r':
			x = parpos[0]+parpos[2]-int(tags["posx"][:-1])
		else:
			x = parpos[0]+int(tags["posx"])
	else:
		x = parpos[0]

	if "posy" in tags:
		if tags["posy"][-1] == 'r':
			y = parpos[1]+parpos[3]-int(tags["posy"][:-1])
		else:
			y = parpos[1]+int(tags["posy"])
	else:
		y = parpos[1]

	if "width" in tags:
		w = int(tags["width"])
		dw = w
	else:
		w = parpos[2]
		dw = None
	if "height" in tags:
		h = int(tags["height"])
		dh = h
	else:
		h = parpos[3]
		dh = None

	return (x,y,w,h),(dw,dh)

def draw(i, parpos):
#	print i

	p = pos(i,parpos)
	if p[1][0] and p[1][1]:
		pygame.draw.rect(screen, (100+random()*155,100+random()*155,100+random()*155,), (p[0][0],p[0][1],p[1][0],p[1][1]), 1)
#	else:
#		pygame.draw.line(screen, (100+random()*155,100+random()*155,100+random()*155,), (p[0],p[1]),(p[0]+100,p[1]),1)
#		pygame.draw.line(screen, (100+random()*155,100+random()*155,100+random()*155,), (p[0],p[1]),(p[0],p[1]+100),1)
#	print p

	if i["@type"] == "group":
		for i in i["control"]:
			draw(i,p[0])

def redraw(x):
	screen.fill((0,0,0))
	for i in x:
		draw(i, (0,0,1280,720))
	pygame.display.flip()








x=xmltodict.parse(open(sys.argv[1], 'r').read())["window"]["controls"]["control"]

rects = dict()

y(x, 0, (0,0,1280,720))
#fill rects

print rects








def process_event(event):
	if event.type == pygame.QUIT:
		pygame.display.iconify()
		exit()
#	if event.type == pygame.VIDEOEXPOSE:
#		redraw(x)	
	if event.type == pygame.MOUSEMOTION:
		x = ""
		for rect,name in rects.iteritems():
			if pygame.Rect(rect).collidepoint(pygame.mouse.get_pos()):
				x = x + " " + name
		pygame.display.set_caption(x)

def loop():
	redraw(x)
	process_event(pygame.event.wait())


while 1:
	try:
		pygame.time.set_timer(pygame.USEREVENT, 333)
		#the idea here is to bump the event quee sometime,
		#because we get stuck in event.wait and so
		#dont process a KeyboardInterrupt
		#which is the nice thing that allows to ctrl-C this

		loop()
	except KeyboardInterrupt() as e:
		pygame.display.iconify()
		#dying takes forever and is ugly so hide it

		raise e
	except Exception() as e:
		pass
		#but i dont want to die at all!

