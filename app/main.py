import bottle
import os
import random
import pygame
from pygame.locals import *
import math


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start(self):
    data = bottle.request.json
    game_id = data['game_id']
    self.board_width = data['width']
    self.board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    
    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, self.board_width, self.board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move(self):
    data = bottle.request.json

    directions = ['up', 'down', 'right', 'left']

    currentdir = 'left'

    ourSnakeX = data['snakes'[0]['coords'][0][0]]
    ourSnakeY = data['snakes'[0]['coords'][0][1]]

    rightSpace = self.board_width - ourSnakeX
    leftSpace = 0 - ourSnakeX
    downSpace = self.board_height - ourSnakeY
    upSpace = 0 - ourSnakeY

    #if upSpace == 0:
     #   direction = 'left'
    #if leftSpace == 0:
     #   direction = 'up'
    #if downSpace == 0:
     #   direction = 'left'
    #if rightSpace == 0:
     #   direction = 'up'

    topWall = [(x, 0) for x in range(self.board_width + 1)]
    leftWall = [(0, y) for y in range(self.board_height + 1)]
    rightWall = [(self.board_width, y) for y in range(self.board_height + 1)]
    bottomWall = [(x, self.board_height) for x in range(self.board_width + 1)]

    playerPos = data['snakes'[0]['coords']] + data['snakes'[1]['coords']] + data['snakes'[2]['coords']] + data['snakes'[3]['coords']] 
    obstacles = topWall + leftWall + rightWall + bottomWall

    def pathlen (self, a, b):
        return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)

    def coorAdd(self, pos, pat):
        if pat == 'left':
            pat = [-1, 0]
        elif pat == 'right':
            pat = [1, 0]
        elif pat == 'up':
            pat = [0, -1]
        elif pat == 'down':
            pat = [0, 1]
        
        return pos[0]+pat[0], pos[1]+pat[1]


    olddir = currentdir
    position = data['snakes'[0]['coords'][0]]

    complement = [('up', 'down'), ('down', 'up'), ('right', 'left'), ('left', 'right')]
    invaliddir = [x for (x, y) in complement if y == olddir]
    validdir = [dir for dir in directions if not(dir in invaliddir)]

    validdir=[dir for dir in validdir if not (coorAdd(position,dir) in obstacles or coorAdd(position,dir) in playerPos)]
    olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
    shortest=self.pathlen(coorAdd(position,olddir) , data['food'])

    for dir in validdir:
            newpos=self.coorAdd(position,dir)
            newlen=self.pathlen(newpos , game.foodpos)#length in shortest path
            if newlen < shortest:
                if not ( newpos in obstacles or newpos in playerPos):
                    olddir=dir
                    shortest=newlen
    currentdir = olddir

    return {
        'move': currentdir,
        'taunt': 'Everything is Awesome!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '134.87.130.164'), port=os.getenv('PORT', '8080'))