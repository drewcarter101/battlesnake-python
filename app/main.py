import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    
    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    ourSnakeX = data['snakes'[0]['coords'][0][0]]
    ourSnakeY = data['snakes'[0]['coords'][0][1]]

    rightSpace = board_width - ourSnakeX
    leftSpace = 0 - ourSnakeX
    downSpace = board_height - ourSnakeY
    upSpace = 0 - ourSnakeY

    #enemyDistanceLeft
    #enemyDistanceRight
    #enemyDistanceUp
    #enemyDistanceDown

    if(upSpace == 0):
        direction='left'
    if(leftSpace==0):
        direction='up'
    if(downSpace==0):
        direction='left'
    if(rightSpace==0):
        direction='up'

    return {
        'move': direction,
        'taunt': 'Everything is Awesome!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '134.87.130.164'), port=os.getenv('PORT', '8080'))